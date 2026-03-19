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