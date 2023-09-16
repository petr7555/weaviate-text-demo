import json

import weaviate

from ai_text_demo.constants import WEAVIATE_URL, OPENAI_API_KEY

client = weaviate.Client(
    url=WEAVIATE_URL,
    additional_headers={
        "X-OpenAI-Api-Key": OPENAI_API_KEY
    }
)

print('Semantic (similarity) search')
response = (
    client.query
    .get("Question", ["question", "answer", "category"])
    .with_near_text({"concepts": ["biology"]})
    .with_limit(2)
    .do()
)

print(json.dumps(response, indent=2))

print('Semantic search with a filter')
response = (
    client.query
    .get("Question", ["question", "answer", "category"])
    .with_near_text({"concepts": ["biology"]})
    .with_where({
        "path": ["category"],
        "operator": "Equal",
        "valueText": "ANIMALS"
    })
    .with_limit(2)
    .do()
)

print(json.dumps(response, indent=2))

print('Generative search (single prompt)')
response = (
    client.query
    .get("Question", ["question", "answer", "category"])
    .with_near_text({"concepts": ["biology"]})
    .with_generate(single_prompt="Explain {answer} as you might to a five-year-old.")
    .with_limit(2)
    .do()
)

print(json.dumps(response, indent=2))

print('Generative search (grouped task)')
response = (
    client.query
    .get("Question", ["question", "answer", "category"])
    .with_near_text({"concepts": ["biology"]})
    .with_generate(grouped_task="Write a tweet with emojis about these facts.")
    .with_limit(2)
    .do()
)

print(response["data"]["Get"]["Question"][0]["_additional"]["generate"]["groupedResult"])
