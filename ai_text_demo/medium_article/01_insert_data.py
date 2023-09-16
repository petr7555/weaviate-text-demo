import json

import pandas as pd
import weaviate
from weaviate.util import generate_uuid5

from ai_text_demo.constants import WEAVIATE_URL, OPENAI_API_KEY
from ai_text_demo.utils import relative_path_from_file

DATA_PATH = relative_path_from_file(__file__, 'data/jeopardy_questions.csv')

client = weaviate.Client(
    url=WEAVIATE_URL,
    additional_headers={
        "X-OpenAI-Api-Key": OPENAI_API_KEY
    }
)

class_obj = {
    # Class definition
    "class": "JeopardyQuestion",

    # Property definitions
    "properties": [
        {
            "name": "category",
            "dataType": ["text"],
        },
        {
            "name": "question",
            "dataType": ["text"],
        },
        {
            "name": "answer",
            "dataType": ["text"],
        },
    ],

    # Specify a vectorizer
    "vectorizer": "text2vec-openai",

    # Module settings
    "moduleConfig": {
        "text2vec-openai": {
            "vectorizeClassName": False,
            "model": "ada",
            "modelVersion": "002",
            "type": "text"
        },
        "qna-openai": {
            "model": "text-davinci-002"
        },
        "generative-openai": {
            "model": "gpt-3.5-turbo"
        }
    },
}

client.schema.delete_class("JeopardyQuestion")
client.schema.create_class(class_obj)

print(json.dumps(client.schema.get("JeopardyQuestion"), indent=2))

df = pd.read_csv(DATA_PATH, nrows=100)

client.batch.configure(batch_size=200,  # Specify batch size
                       num_workers=2)  # Parallelize the process

with client.batch as batch:
    for _, row in df.iterrows():
        question_object = {
            "category": row.category,
            "question": row.question,
            "answer": row.answer,
        }
        batch.add_data_object(
            question_object,
            class_name="JeopardyQuestion",
            # Although Weaviate will generate a uuid automatically,
            # we will generate it manually from the question_object to avoid importing duplicate items.
            uuid=generate_uuid5(question_object)
        )

print(client.query.aggregate("JeopardyQuestion").with_meta_count().do())
