import json

import requests
import weaviate

from ai_text_demo.constants import WEAVIATE_URL, OPENAI_API_KEY

client = weaviate.Client(
    url=WEAVIATE_URL,
    additional_headers={
        "X-OpenAI-Api-Key": OPENAI_API_KEY
    }
)

class_obj = {
    "class": "Question",
    # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
    "vectorizer": "text2vec-openai",
    "moduleConfig": {
        "text2vec-openai": {},
        "generative-openai": {}  # Ensure the `generative-openai` module is used for generative queries
    }
}

# Ensure the class is deleted and re-created
client.schema.delete_class("Question")
client.schema.create_class(class_obj)

# Use `vectorizer`
resp = requests.get('https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json')

# Provide own pre-generated vectors
# resp = requests.get(
#     'https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny_with_vectors_all-OpenAI-ada-002.json')

data = json.loads(resp.text)  # Load data

client.batch.configure(batch_size=100)  # Configure batch
with client.batch as batch:  # Initialize a batch process
    for i, d in enumerate(data):  # Batch import data
        print(f"importing question: {i + 1}")
        properties = {
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
        }
        batch.add_data_object(
            data_object=properties,
            class_name="Question",
            # vector=d["vector"]  # Add custom vector
        )
