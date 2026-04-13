from fastapi import FastAPI,Query,Request,Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import requests as req
from instruments.read_files import FileReader,normalize
from instruments.sheme import QuerySheme,AddFileSheme
from instruments.global_variables import sentens_transformer
from instruments.milvus_database import collection_chunks,collection_sentences
from instruments.functions import urlnormilize
from instruments.database_conection import Connect 
from instruments.sql_database import get_db,Chunck
from sqlalchemy.orm import Session
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates=Jinja2Templates("./instruments/html")

@app.get("/")
def render(request: Request,url:str=Query("")):
    site=req.get(url,headers={
        "User-Agent": "Mozilla/5.0"
    })

    soup=BeautifulSoup(site.content,"html.parser")
    html_body=soup.body.decode_contents()

    return templates.TemplateResponse("index.html",{"request":request,"html_body":html_body})

@app.post("/query")
def complete_query(data:QuerySheme,session:Session=Depends(get_db)):
    query_embedding=normalize(sentens_transformer.encode([data.query]))
    database=Connect(session)
    results=database.search(query_embedding,data.topics)
    response=[]
    for item in results:
        response.append({
            "id":item.id,
            "url":item.url,
            "name":item.name
        })
    return response

@app.post("/file")
def add_file(path_file:AddFileSheme,session:Session=Depends(get_db)):
    #try:
    url=urlnormilize(path_file.query)

    if session.query(Chunck).filter(Chunck.url==url).all():
        return {"ok":False,"error":"Такий файл вже є"}
    
    file=req.get(url,headers={
        "User-Agent": "Mozilla/5.0"
    })
    content_type = file.headers.get("Content-Type")

    reader=FileReader()
    groups=reader.get_embedding(content_type=content_type.lower(),url=url,file=file)

    database=Connect(session)
    database.add(groups,url,path_file.topic)
    return {"ok":True}
    """except Exception as e:
        print(e)
        return {"ok":False}"""
    
@app.get("/topics")
def get_topic(session:Session=Depends(get_db)):
    result=session.query(Chunck.topic).distinct().all()
    return [topic for (topic,) in result]