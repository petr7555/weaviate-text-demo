import json
import textwrap

import weaviate

from ai_text_demo.constants import WEAVIATE_URL, OPENAI_API_KEY

client = weaviate.Client(
    url=WEAVIATE_URL,
    additional_headers={
        "X-OpenAI-Api-Key": OPENAI_API_KEY
    }
)

res = (
    client.query.get(
        "Document",
        "source")
    .with_bm25(query="some paper about housing prices")
    .with_additional("score")
    .do()
)

print(json.dumps(res, indent=2))

prompt = """
Please summarize the following academic abstract in a one-liner for a layperson:

{abstract}
"""

results = (
    client.query.get(
        "Document",
        "source")
    .with_generate(single_prompt=prompt)
    .do()
)

docs = results["data"]["Get"]["Document"]

for doc in docs:
    source = doc["source"]
    abstract = doc["_additional"]["generate"]["singleResult"]
    wrapped_abstract = textwrap.fill(abstract, width=80)
    print(f"Source: {source}\nSummary:\n{wrapped_abstract}\n")
