import pdfplumber
#from docx import Document
from lxml import etree,html
from io import BytesIO
from .global_variables import sentens_transformer
import numpy as np
from unidecode import unidecode
from .functions import *
import re


def read_pdf(url,file=None):
    with pdfplumber.open(BytesIO(file.content)) as f:
        pages = f.pages[10:]
        chuncks=get_chuncks_pdf(pages)
        return get_sentences_pdf(url,chuncks)

def normalize( embedding):
    return embedding / np.linalg.norm(embedding)

def read_docs(file=None):
    print("DOCS")

def read_html(url,file=None):
    tree=html.fromstring(file.content)
    tree_wrapper = etree.ElementTree(tree)
    for bad in tree.xpath('//header | //nav | //footer'):
        bad.getparent().remove(bad)
    chuncks=get_chuncks_html(tree)
    return get_sentences_html(url,tree,tree_wrapper,chuncks)


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
            return self.__methods_for_read_file[content_type](url,file) 
        print("Невідомий файл")
    
    def get_embedding(self,content_type,url,file=None):
        groups=self.read(content_type=content_type,url=url,file=file)
        for key in groups:
            groups[key]["texts"]=normalize(sentens_transformer.encode(groups[key]["texts"]))
            groups[key]["vector"]=normalize(sentens_transformer.encode(key))
        return groups