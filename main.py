from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
import requests as req
from instruments.read_files import FileReader
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
    port="5000"
)

db_name="files"
if db_name not in db.list_database():
    db.create_database(db_name=db_name)

db.using_database(db_name=db_name)

schema=CollectionSchema([
    FieldSchema(name="id",dtype=DataType.INT64,is_primary=True,auto_id=True),
    FieldSchema(name="vector",dtype=DataType.FLOAT_VECTOR,dim=384),
    FieldSchema(name="url",dtype=DataType.VARCHAR,max_length=1000),
    FieldSchema(name="name",dtype=DataType.VARCHAR,max_length=100)
])
collection = Collection(name="multilingual_vectors", schema=schema)

collection.create_index({
    "vector",
    {
        "metric_type":"IP",
        "index_type":"HNSW",
        "params":{"M":8,"efConstruction":64}
    }
})

collection.load()

app = FastAPI()

@app.get("/")
def root():
    return "Hello World"

@app.post("/query")
def complete_query(query:str):
    sentens_transformer=SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    query_embedding=sentens_transformer.encode([query])
    return {"ok":True}

@app.post("/file")
def add_file(path_file:str):
    try:
        file=req.get(path_file,headers={
            "User-Agent": "Mozilla/5.0"
        })
        content_type = file.headers.get("Content-Type")
        reader=FileReader()
        collection.insert([reader.get_embedding(content_type=content_type,file=file),path_file,reader.read(content_type=content_type,file=file).split(" ")[0:10].join(" ")])
        collection.load()
        return {"ok":True}
    except:
        return {"ok":False}