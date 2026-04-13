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
     FieldSchema(name="id",dtype=DataType.INT64,is_primary=True),
     FieldSchema(name="vector",dtype=DataType.FLOAT_VECTOR,dim=384)
])

collection_chunks = Collection(name="chunks2", schema=schema)
collection_sentences=Collection(name="sentences2", schema=schema)

colection_params={
    "metric_type":"IP",
    "index_type":"HNSW",
    "params":{"M":8,"efConstruction":64}
}

collection_chunks.create_index("vector",colection_params)
collection_sentences.create_index("vector",colection_params)


collection_chunks.load()
collection_sentences.load()