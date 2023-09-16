import json

import weaviate

from ai_text_demo.constants import WEAVIATE_URL, OPENAI_API_KEY

client = weaviate.Client(
    url=WEAVIATE_URL,
    additional_headers={
        "X-OpenAI-Api-Key": OPENAI_API_KEY
    }
)

print("Query two objects")
res = (
    client.query.get("JeopardyQuestion",
                     ["jeopardyQuestion", "jeopardyAnswer", "jeopardyCategory"])
    .with_additional(["id"])
    .with_limit(2)
    .do()
)

print(json.dumps(res, indent=2))

print("Vector search")
res = (
    client.query.get(
        "JeopardyQuestion",
        ["jeopardyQuestion", "jeopardyAnswer", "jeopardyCategory"])
    .with_near_text({"concepts": "animals"})
    .with_limit(2)
    .do()
)

print(json.dumps(res, indent=2))

print("Question answering")
res = (
    client.query
    .get("JeopardyQuestion", [
        "jeopardyAnswer",
        "_additional {answer {hasAnswer property result} }"
    ])
    .with_ask({
        "question": "Which animal was mentioned in the title of the Aesop fable?",
        "properties": ["jeopardyAnswer"]
    })
    .with_limit(1)
    .do()
)
print(json.dumps(res, indent=2))

print("Generative search")
res = (
    client.query.get(
        "JeopardyQuestion",
        ["jeopardyQuestion", "jeopardyAnswer"])
    .with_near_text({"concepts": ["animals"]})
    .with_limit(1)
    .with_generate(single_prompt="Generate a question to which the answer is {jeopardyAnswer}")
    .do()
)

print(json.dumps(res, indent=2))
