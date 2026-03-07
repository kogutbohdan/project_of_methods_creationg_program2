import pdfplumber
#from docx import Document
from bs4 import BeautifulSoup
from io import BytesIO
from sentence_transformers import SentenceTransformer
import numpy as np
def read_pdf(file=None):
    with pdfplumber.open(BytesIO(file.content)) as f:
        text="" 
        for page in f.pages:
            text+=page.extract_text()
    return text

def normalize( embedding):
    return embedding / np.linalg.norm(embedding)

def read_docs(file=None):
    print("DOCS")

def read_html(file=None):
    soup=BeautifulSoup(file.content,"html.parser")
    for tag in soup.find_all(True):
        tag.unwrap()
    return soup.get_text(separator=" ")


class FileReader:
    __methods_for_read_file={
        "application/pdf":read_pdf,
        "application/msword":read_docs,
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document":read_docs,
        "text/html; charset=utf-8":read_html,
        "text/html":read_html
    }

    def read(self,content_type,file=None):
        print("rabar"+content_type+"rabar")
        if content_type in self.__methods_for_read_file.keys():
            return self.__methods_for_read_file[content_type](file)
        print("Невідомий файл")
    
    def get_embedding(self,content_type,file=None):
        sentens_transformer=SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        return normalize(sentens_transformer.encode([self.read(content_type=content_type,file=file)]))