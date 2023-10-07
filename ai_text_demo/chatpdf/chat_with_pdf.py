import os
import sys

import requests
from dotenv import load_dotenv

SOURCE_ID = sys.argv[1]

load_dotenv()
CHATPDF_API_KEY = os.getenv("CHATPDF_API_KEY")

headers = {
    'x-api-key': CHATPDF_API_KEY,
    "Content-Type": "application/json",
}

data = {
    'sourceId': SOURCE_ID,
    'messages': [
        {
            'role': "user",
            'content': "What is CNN?",
        },
    ]
}

response = requests.post(
    'https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

if response.status_code == 200:
    print('Result:', response.json()['content'])
else:
    print('Status:', response.status_code)
    print('Error:', response.text)
