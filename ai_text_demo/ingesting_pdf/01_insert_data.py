import logging
from pathlib import Path

import weaviate
from unstructured.partition.pdf import partition_pdf

from ai_text_demo.constants import WEAVIATE_URL, OPENAI_API_KEY
from ai_text_demo.ingesting_pdf.abstract_extractor import AbstractExtractor
from ai_text_demo.utils import relative_path_from_file

DATA_FOLDER = relative_path_from_file(__file__, "data")

logging.basicConfig(level=logging.INFO)

client = weaviate.Client(
    url=WEAVIATE_URL,
    additional_headers={
        "X-OpenAI-Api-Key": OPENAI_API_KEY
    }
)

schema = {
    "class": "Document",
    "vectorizer": "text2vec-openai",
    "properties": [
        {
            "name": "source",
            "dataType": ["text"],
        },
        {
            "name": "abstract",
            "dataType": ["text"],
            "moduleConfig": {
                "text2vec-openai": {
                    "skip": False,
                    "vectorizePropertyName": False
                }
            },
        },
    ],
    "moduleConfig": {
        "text2vec-openai": {
            "model": "ada",
            "modelVersion": "002",
            "type": "text"
        },
        "generative-openai": {},
    },
}

client.schema.delete_class("Document")
client.schema.create_class(schema)

data_objects = []

for path in Path(DATA_FOLDER).iterdir():
    if path.suffix != ".pdf":
        continue

    logging.info(f"Processing {path.name}...")

    elements = partition_pdf(filename=path, strategy="ocr_only")

    abstract_extractor = AbstractExtractor()
    abstract_extractor.consume_elements(elements)

    data_object = {"source": path.name, "abstract": abstract_extractor.abstract()}

    data_objects.append(data_object)

client.batch.configure(batch_size=100)  # Configure batch
with client.batch as batch:
    for data_object in data_objects:
        batch.add_data_object(data_object, "Document")
