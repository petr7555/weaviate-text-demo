import os

from dotenv import load_dotenv

load_dotenv()

WEAVIATE_URL = 'http://localhost:8080'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
