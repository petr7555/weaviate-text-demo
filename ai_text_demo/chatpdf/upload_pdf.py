import os

import requests

from ai_text_demo.utils import relative_path_from_file
from dotenv import load_dotenv

DATA_PATH = relative_path_from_file(__file__, "data/paper01.pdf")

load_dotenv()
CHATPDF_API_KEY = os.getenv("CHATPDF_API_KEY")

# You can only upload one file at a time.
files = [
    ('file', ('file', open(DATA_PATH, 'rb'), 'application/octet-stream')),
]
headers = {
    'x-api-key': CHATPDF_API_KEY
}

response = requests.post(
    'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)

if response.status_code == 200:
    # Returns a source ID that can be used to interact with the PDF file.
    print('Source ID:', response.json()['sourceId'])
else:
    print('Status:', response.status_code)
    print('Error:', response.text)
