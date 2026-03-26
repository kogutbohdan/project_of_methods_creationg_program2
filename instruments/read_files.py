import pdfplumber
#from docx import Document
from bs4 import BeautifulSoup
from io import BytesIO
from .global_variables import sentens_transformer
import numpy as np
from unidecode import unidecode

def read_pdf(url,file=None):
    with pdfplumber.open(BytesIO(file.content)) as f:
        pages = f.pages[10:]
        pages_text=[]
        names=[]
        urls=[]
        i=0
        for page in pages:
            page_text = page.extract_text()
            if page_text:
                pages_text.append(unidecode(page_text))
                names.append(" ".join(page_text.split(" ")[0:10]))
                urls.append(f"{url}#page={page.page_number}")
            if i>=20:
                break
            i+=1
    return pages_text,names,urls

def normalize( embedding):
    return embedding / np.linalg.norm(embedding)

def read_docs(file=None):
    print("DOCS")

def read_html(url,file=None):
    soup=BeautifulSoup(file.content,"html.parser")
    h=["h1","h2","h3"]
    texts=[]
    names=[]
    for tag in soup.find_all(h):
        names.append(tag.get_text())
        content=[]
        for sibling in tag.next_siblings:
            if sibling.name in h:
                break
            if hasattr(sibling,"get_text"):
                text=sibling.get_text()
                if text:
                    content.append(text)
        full_text=" ".join(content)
        texts.append(full_text)
    return texts,names,[url for i in range(len(texts))]


class FileReader:
    __methods_for_read_file={
        "application/pdf":read_pdf,
        "application/msword":read_docs,
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document":read_docs,
        "text/html; charset=utf-8":read_html,
        "text/html":read_html
    }

    def read(self,content_type,url,file=None):
        print("rabar"+content_type+"rabar")
        if content_type in self.__methods_for_read_file.keys():
            pages_text,names,urls=self.__methods_for_read_file[content_type](url,file)
            return pages_text,names,urls
        print("Невідомий файл")
    
    def get_embedding(self,content_type,url,file=None):
        pages_text,names,urls=self.read(content_type=content_type,url=url,file=file)
        return normalize(sentens_transformer.encode(pages_text)),names,urls