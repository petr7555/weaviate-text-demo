# AI text demos

## How to run

### Common steps

- `poetry install` to install dependencies

- `docker compose -f docker-compose-weaviate.yml up -d`

[//]: # (- create `.env` file with `OPENAI_API_KEY=YOUR_OPENAI_API_KEY`)

[//]: # (    - you can get it from https://platform.openai.com/)

### 1. Search article titles from Medium using Milvus

Based on https://milvus.io/docs/text_search_engine.md.

- `docker compose -f docker-compose-milvus.yml up -d`
    - Attu dashboard is running at: http://localhost:3000, no credentials required.
- `poetry run python ai_text_demo/milvus_search_titles/00_data_analysis.py`
    - There are 5979 titles, each is embedded into 768-dimensional vector.
- `poetry run python ai_text_demo/milvus_search_titles/01_insert_data.py`
    - Creates a Milvus collection and inserts data using Towhee pipe.
- `poetry run python ai_text_demo/milvus_search_titles/02_search_title.py`
    - Searches for similar titles to one input, to array of inputs, returns metadata, searches using expression to
      filter results.
    - `poetry run python ai_text_demo/milvus_search_titles/03_query.py`
        - Queries Milvus collection using expression to filter results.

### 1. Weaviate Quickstart

Based on https://weaviate.io/developers/weaviate/quickstart.

- `docker compose -f docker-compose-weaviate.yml up -d`
- `poetry run python ai_text_demo/weaviate_quickstart/01_insert_data.py`
- `poetry run python ai_text_demo/weaviate_quickstart/02_queries.py`

### 2. Medium article

Based
on https://towardsdatascience.com/getting-started-with-weaviate-a-beginners-guide-to-search-with-vector-databases-14bbb9285839.

- `poetry run python ai_text_demo/medium_article/01_insert_data.py`
- `poetry run python ai_text_demo/medium_article/02_queries.py`

### 3. Ingesting PDFs into Weaviate

Based on https://weaviate.io/blog/ingesting-pdfs-into-weaviate.

- `poetry run python ai_text_demo/ingesting_pdf/01_insert_data.py`
- `poetry run python ai_text_demo/ingesting_pdf/02_queries.py`
- `poetry run python ai_text_demo/ingesting_pdf/03_chatbot.py`
- `uvicorn ai_text_demo.ingesting_pdf.chatbot_server:app --reload` to start chatbot server

### 4. `stage_for_weaviate` unstructured brick

Based on https://unstructured-io.github.io/unstructured/bricks/staging.html#stage-for-weaviate
and https://github.com/Unstructured-IO/unstructured/blob/main/examples/weaviate/weaviate.ipynb.

- `poetry run python ai_text_demo/weaviate_brick/01_insert_data.py`
- `poetry run python ai_text_demo/weaviate_brick/02_queries.py`

### 5. Basic PDF read

- `poetry run python ai_text_demo/pdf_read/main.py`

### 6. LangChain Weaviate

Based on https://python.langchain.com/docs/integrations/vectorstores/weaviate.

- `poetry run python ai_text_demo/langchain_weaviate/similarity_search.py`
- `poetry run python ai_text_demo/langchain_weaviate/question_answering_with_sources.py`

### X. Ingesting PDFs from Nordic Trustee
