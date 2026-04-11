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

base_param=[
    FieldSchema(name="id",dtype=DataType.INT64,is_primary=True,auto_id=True),
    FieldSchema(name="vector",dtype=DataType.FLOAT_VECTOR,dim=384),
    FieldSchema(name="url",dtype=DataType.VARCHAR,max_length=10000)
]


schema_chunks=CollectionSchema([
    *base_param,
    FieldSchema(name="topic",dtype=DataType.VARCHAR,max_length=1000)
])

schema_sentences=CollectionSchema([
    *base_param,
    FieldSchema(name="chunck_id",dtype=DataType.INT64),
    FieldSchema(name="name",dtype=DataType.VARCHAR,max_length=10000)
])

collection_chunks = Collection(name="chunks", schema=schema_chunks)
collection_sentences=Collection(name="sentences", schema=schema_sentences)

colection_params={
    "metric_type":"IP",
    "index_type":"HNSW",
    "params":{"M":8,"efConstruction":64}
}

collection_chunks.create_index("vector",colection_params)
collection_sentences.create_index("vector",colection_params)


collection_chunks.load()
collection_sentences.load()