import pandas as pd
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from towhee import ops, pipe

from constants import MILVUS_HOST, MILVUS_PORT, COLLECTION_NAME, TITLE_VECTOR_LENGTH, DATA_PATH

connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)


def create_milvus_collection(collection_name, dim):
    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
        FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=500),
        FieldSchema(name="title_vector", dtype=DataType.FLOAT_VECTOR, dim=dim),
        FieldSchema(name="link", dtype=DataType.VARCHAR, max_length=500),
        FieldSchema(name="reading_time", dtype=DataType.INT64),
        FieldSchema(name="publication", dtype=DataType.VARCHAR, max_length=500),
        FieldSchema(name="claps", dtype=DataType.INT64),
        FieldSchema(name="responses", dtype=DataType.INT64)
    ]
    schema = CollectionSchema(fields=fields, description='search text')
    collection = Collection(name=collection_name, schema=schema)

    index_params = {
        'metric_type': "L2",
        'index_type': "IVF_FLAT",
        'params': {"nlist": 2048}
    }
    collection.create_index(field_name='title_vector', index_params=index_params)
    return collection


collection = create_milvus_collection(COLLECTION_NAME, TITLE_VECTOR_LENGTH)

insert_pipe = (pipe.input('df')
               .flat_map('df', 'data', lambda df: df.values.tolist())
               .map('data', 'res', ops.ann_insert.milvus_client(host=MILVUS_HOST,
                                                                port=MILVUS_PORT,
                                                                collection_name=COLLECTION_NAME))
               .output('res')
               )

df = pd.read_csv(DATA_PATH, converters={'title_vector': lambda x: eval(x)})
insert_pipe(df)

collection.load()
print(f"Collection {COLLECTION_NAME} num_entities: {collection.num_entities}")
