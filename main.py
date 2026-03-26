from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests as req
from instruments.read_files import FileReader,normalize
from instruments.sheme import QuerySheme
from instruments.global_variables import sentens_transformer
from instruments.database import collection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return "Hello World"

@app.post("/query")
def complete_query(data:QuerySheme):
    query_embedding=normalize(sentens_transformer.encode([data.query]))
    result=collection.search(query_embedding,"vector",{
        "metric_type":"IP",
        "params":{"ef":64}
    },10,output_fields=["url","name"])
    print("RESULT_SEARCH",query_embedding)
    response=[]
    for item in result[0]:
        response.append({
            "score":item.score,
            "url":item.entity.get("url"),
            "name":item.entity.get("name")
        })
    return response

@app.post("/file")
def add_file(path_file:QuerySheme):
    try:
        file=req.get(path_file.query,headers={
            "User-Agent": "Mozilla/5.0"
        })
        content_type = file.headers.get("Content-Type")
        reader=FileReader()
        embeddings,names,urls=reader.get_embedding(content_type=content_type.lower(),url=path_file.query,file=file)
        print("Текст сторінок",len(embeddings),"|",len(urls),"|",len(names))
        collection.insert([embeddings,urls,names])
        collection.load()
        return {"ok":True}
    except Exception as e:
        print(e)
        return {"ok":False}