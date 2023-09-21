# AI text demos

## How to run

### Common steps

- `poetry install` to install dependencies

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

### 2. Weaviate Quickstart

Based on https://weaviate.io/developers/weaviate/quickstart.

- `docker compose -f docker-compose-weaviate.yml up -d`
- create `.env` file with `OPENAI_API_KEY=YOUR_OPENAI_API_KEY`
    - you can get it from https://platform.openai.com/
- `poetry run python ai_text_demo/weaviate_quickstart/01_insert_data.py`
    - Creates a Weaviate "Question" class and inserts data, automatically embedding the objects using OpenAI model.
- `poetry run python ai_text_demo/weaviate_quickstart/02_queries.py`
    - Searches objects most similar to "biology", filters on the "category" property, passes the results one by one to
      OpenAI LLM to generate results, passes the results all together to OpenAI LLM to generate a result.

### 3. Medium article on Weaviate

Based
on https://towardsdatascience.com/getting-started-with-weaviate-a-beginners-guide-to-search-with-vector-databases-14bbb9285839.

- `docker compose -f docker-compose-weaviate.yml up -d`
- create `.env` file with `OPENAI_API_KEY=YOUR_OPENAI_API_KEY`
    - you can get it from https://platform.openai.com/
- `poetry run python ai_text_demo/medium_article/01_insert_data.py`
    - Creates a Weaviate "JeopardyQuestion" class and inserts data, automatically embedding the objects using OpenAI
      model.
- `poetry run python ai_text_demo/medium_article/02_queries.py`
    - Queries two random objects, searches objects most similar to "animals", answers question using OpenAI QnA model,
      generates question using OpenAI LLM.

### 4. Ingesting PDFs into Weaviate

Based on https://weaviate.io/blog/ingesting-pdfs-into-weaviate.

- `docker compose -f docker-compose-weaviate.yml up -d`
- create `.env` file with `OPENAI_API_KEY=YOUR_OPENAI_API_KEY`
    - you can get it from https://platform.openai.com/
- `poetry run python ai_text_demo/ingesting_pdf/01_insert_data.py`
    - Creates a Weaviate "Document" class, partitions PDFs into elements using `unstructured`, extracts abstracts from
      the elements and inserts data into Weaviate, automatically embedding the objects using OpenAI model.
- `poetry run python ai_text_demo/ingesting_pdf/02_queries.py`
    - Queries the database to find "some paper about housing prices", summarizes documents in the database using
      generative model from OpenAI.
- `poetry run python ai_text_demo/ingesting_pdf/03_chatbot.py`
    - Chat with the created vectorstore using LangChain.

#### Chatbot web app

- `uvicorn ai_text_demo.ingesting_pdf.chatbot_server:app --reload` to start chatbot server
- `cd chatbot-frontend`
- `npm install` to install dependencies
- `npm start` to start chatbot frontend
- open http://localhost:3001 in browser

### 5. `stage_for_weaviate` unstructured brick

Based on https://unstructured-io.github.io/unstructured/bricks/staging.html#stage-for-weaviate
and https://github.com/Unstructured-IO/unstructured/blob/main/examples/weaviate/weaviate.ipynb.

- `docker compose -f docker-compose-weaviate.yml up -d`
- `poetry run python ai_text_demo/weaviate_brick/01_insert_data.py`
    - Creates a Weaviate "UnstructuredDocument" class using `create_unstructured_weaviate_class` helper function from
      the `unstructured` library, partitions PDFs into elements using `unstructured`, transforms the elements into
      objects (containing also filename and the page number) using `stage_for_weaviate` function from the `unstructured`
      library, and inserts the objects into Weaviate.
- `poetry run python ai_text_demo/weaviate_brick/02_queries.py`
    - Queries the database to find two objects related to "document understanding".

### 6. Basic PDF read

- `poetry run python ai_text_demo/pdf_read/main.py`
    - Extracts text from PDF using `pypdf` library.

### 7. LangChain Weaviate

Based on https://python.langchain.com/docs/integrations/vectorstores/weaviate.

- `docker compose -f docker-compose-weaviate.yml up -d`
- create `.env` file with `OPENAI_API_KEY=YOUR_OPENAI_API_KEY`
    - you can get it from https://platform.openai.com/
- `poetry run python ai_text_demo/langchain_weaviate/similarity_search.py`
    - Loads and splits text, and creates Weaviate vectorstore from it by embedding it using OpenAI model.
    - Performs similarity search, similarity search with score (cosine distance), and MMR search (also optimizing for
      diversity).
- `poetry run python ai_text_demo/langchain_weaviate/question_answering_with_sources.py`
    - Loads text and splits it into smaller chunks. Creates Weaviate vectorstore from the chunks, adding "source"
      metadata to each chunk. The chunks are embedded using OpenAI model.
    - Answers questions and provides the sources.

### 8. LangChain question answering

Based on https://python.langchain.com/docs/use_cases/question_answering/.

- create `.env` file with `OPENAI_API_KEY=YOUR_OPENAI_API_KEY`
    - you can get it from https://platform.openai.com/
- `poetry run python ai_text_demo/langchain_question_answering/qa_over_blogpost.py`
    - Creates whole QA chain using `VectorstoreIndexCreator`, which uses OpenAI and ChromaDB.
- `poetry run python ai_text_demo/langchain_question_answering/qa_over_blogpost_piece_by_piece.py`
    - Like the previous by with fewer abstractions. Also uses custom prompts and returns source documents and citations.

### 9. LangChain chatbot

Based on https://python.langchain.com/docs/use_cases/chatbots.

- create `.env` file with `OPENAI_API_KEY=YOUR_OPENAI_API_KEY`
    - you can get it from https://platform.openai.com/
- `poetry run python ai_text_demo/langchain_chatbot/01_quickstart.py`
    - Shows plain chat model with one and multiple messages and `ConversationChain` with built-in memory.
- `poetry run python ai_text_demo/langchain_chatbot/02_memory.py`
    - Shows how to use memories.
- `poetry run python ai_text_demo/langchain_chatbot/03_conversation.py`
    - Unpacks what goes under the hood with `ConversationChain` by creating a chain with custom memory and prompt.
- `poetry run python ai_text_demo/langchain_chatbot/04_chat_retrieval.py`
    - Uses `ConversationalRetrievalChain` to chat with a blog post.

### 10. LangChain cite sources

Based on https://python.langchain.com/docs/use_cases/question_answering/how_to/qa_citations.

- create `.env` file with `OPENAI_API_KEY=YOUR_OPENAI_API_KEY`
    - you can get it from https://platform.openai.com/
- `poetry run python ai_text_demo/langchain_cite_sources/main.py`
    - Uses `create_citation_fuzzy_match_chain` to extract citations from text (not just source documents).

### 11. LangChain LLMs vs chat models

Based on https://python.langchain.com/docs/modules/model_io/models/llms/,
https://python.langchain.com/docs/modules/model_io/models/chat/ and
https://python.langchain.com/docs/modules/model_io/models/.

- create `.env` file with `OPENAI_API_KEY=YOUR_OPENAI_API_KEY`
    - you can get it from https://platform.openai.com/
- `poetry run python ai_text_demo/langchain_llm_vs_chat_models/llm.py`
  - string in -> string out
- `poetry run python ai_text_demo/langchain_llm_vs_chat_models/chat_model.py`
  - messages in -> messages out
