import weaviate
from fastapi import FastAPI
from langchain.chains import ChatVectorDBChain
from langchain.llms import OpenAI
from langchain.vectorstores.weaviate import Weaviate
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from ai_text_demo.constants import WEAVIATE_URL, OPENAI_API_KEY

client = weaviate.Client(
    url=WEAVIATE_URL,
    additional_headers={
        "X-OpenAI-Api-Key": OPENAI_API_KEY
    }
)
vectorstore = Weaviate(client, "Document", "abstract")
MyOpenAI = OpenAI(temperature=0.2, openai_api_key=OPENAI_API_KEY)
qa = ChatVectorDBChain.from_llm(MyOpenAI, vectorstore)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
@app.get("/health")
def read_root():
    return "OK"


class AskRequest(BaseModel):
    question: str


@app.post("/ask")
def read_item(ask_request: AskRequest):
    result = qa({"question": ask_request.question, "chat_history": []})
    return {"answer": result["answer"]}
