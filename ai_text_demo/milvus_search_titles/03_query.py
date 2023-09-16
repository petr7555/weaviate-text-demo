import json

from pymilvus import Collection, connections

from constants import COLLECTION_NAME, MILVUS_HOST, MILVUS_PORT

connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)

collection = Collection(name=COLLECTION_NAME)

res = collection.query(
    expr='claps > 3000 && reading_time < 15 && publication like "Towards Data Science%"',
    output_fields=['id', 'title', 'link', 'reading_time', 'publication', 'claps', 'responses'],
    consistency_level='Strong'
)

print(json.dumps(res, indent=2))
