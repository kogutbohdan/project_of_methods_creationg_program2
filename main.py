from fastapi import FastAPI,Query,Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import requests as req
from instruments.read_files import FileReader,normalize
from instruments.sheme import QuerySheme,AddFileSheme
from instruments.global_variables import sentens_transformer
from instruments.database import collection_chunks,collection_sentences
from instruments.functions import urlnormilize
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
def complete_query(data:QuerySheme):
    query_embedding=normalize(sentens_transformer.encode([data.query]))
    param_search={
        "metric_type":"IP",
        "params":{"ef":64}
    }
    result_chuncks=collection_chunks.search(query_embedding,"vector",param_search,5,output_fields=["id"],expr=f"topic in {data.topics}")
    ids = [hit.id for hit in result_chuncks[0]]
    result=collection_sentences.search(query_embedding,"vector",param_search,10,output_fields=["id","url","name"],expr=f"chunck_id in {ids}")
    print("RESULT_SEARCH",query_embedding)
    response=[]
    for item in result[0]:
        response.append({
            "id":item.entity.get("id"),
            "score":item.score,
            "url":item.entity.get("url"),
            "name":item.entity.get("name")
        })
    return response

@app.post("/file")
def add_file(path_file:AddFileSheme):
    #try:
    url=urlnormilize(path_file.query)
    print(url)
    if collection_chunks.query(expr=f"url=='{url}'"):
        return {"ok":False,"error":"Такий файл вже є"}
    file=req.get(url,headers={
        "User-Agent": "Mozilla/5.0"
    })
    content_type = file.headers.get("Content-Type")
    reader=FileReader()
    groups=reader.get_embedding(content_type=content_type.lower(),url=url,file=file)
    for key in groups:
        print(groups[key]["vector"])
        res=collection_chunks.insert([[groups[key]["vector"]],[url],[path_file.topic.strip()]])
        chunk_ids=list(res.primary_keys)*len(groups[key]["texts"])
        collection_sentences.insert([groups[key]["texts"],groups[key]["urls"],chunk_ids,groups[key]["names"]])
        collection_chunks.load()
        collection_sentences.load()
    return {"ok":True}
    """except Exception as e:
        print(e)
        return {"ok":False}"""
    
@app.get("/topics")
def get_topic():
    result=collection_chunks.query(expr="topic!=''",output_fields=["topic"])
    return list({r["topic"] for r in result})