from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests as req
from instruments.read_files import FileReader,normalize
from instruments.sheme import QuerySheme
from instruments.global_variables import sentens_transformer
from pymilvus import (
    connections,
    db,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection
)

connections.connect(
    alias="default",
    host="localhost",
    port="19530"
)

db_name="files"
if db_name not in db.list_database():
    db.create_database(db_name=db_name)

db.using_database(db_name=db_name)

schema=CollectionSchema([
    FieldSchema(name="id",dtype=DataType.INT64,is_primary=True,auto_id=True),
    FieldSchema(name="vector",dtype=DataType.FLOAT_VECTOR,dim=384),
    FieldSchema(name="url",dtype=DataType.VARCHAR,max_length=2000),
    FieldSchema(name="name",dtype=DataType.VARCHAR,max_length=2000)
])
collection = Collection(name="multilingual_vectors2", schema=schema)

collection.create_index(
    "vector",
    {
        "metric_type":"IP",
        "index_type":"HNSW",
        "params":{"M":8,"efConstruction":64}
    }
)


collection.load()

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
        print(len(path_file.query))
        print(reader.read(content_type=content_type,file=file).split(" ")[0:10])
        collection.insert([reader.get_embedding(content_type=content_type,file=file),[path_file.query],[" ".join(reader.read(content_type=content_type,file=file).split(" ")[0:10])]])
        collection.load()
        return {"ok":True}
    except Exception as e:
        print(e)
        return {"ok":False}