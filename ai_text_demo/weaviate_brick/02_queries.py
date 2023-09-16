import json

import weaviate

from ai_text_demo.constants import WEAVIATE_URL

client = weaviate.Client(
    url=WEAVIATE_URL,
)

response = (
    client.query
    .get("UnstructuredDocument", ["text", "_additional {score}"])
    .with_bm25(query="document understanding")
    .with_limit(2)
    .do()
)

print(json.dumps(response, indent=2))
