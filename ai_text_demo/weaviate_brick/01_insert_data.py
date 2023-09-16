import tqdm
import weaviate
from unstructured.partition.pdf import partition_pdf
from unstructured.staging.weaviate import create_unstructured_weaviate_class
from unstructured.staging.weaviate import stage_for_weaviate
from weaviate.util import generate_uuid5

from ai_text_demo.constants import WEAVIATE_URL
from ai_text_demo.utils import relative_path_from_file

DATA_PATH = relative_path_from_file(__file__, "data/layout-parser-paper-fast.pdf")

unstructured_class_name = "UnstructuredDocument"
unstructured_class = create_unstructured_weaviate_class(class_name=unstructured_class_name)

client = weaviate.Client(
    url=WEAVIATE_URL,
)

client.schema.delete_class(unstructured_class_name)
client.schema.create_class(unstructured_class)

elements = partition_pdf(filename=DATA_PATH, strategy="fast")
data_objects = stage_for_weaviate(elements)

client.batch.configure(batch_size=10)
with client.batch as batch:
    for data_object in tqdm.tqdm(data_objects):
        batch.add_data_object(
            data_object,
            unstructured_class_name,
            uuid=generate_uuid5(data_object),
        )
