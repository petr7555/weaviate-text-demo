import dotenv
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT
from langchain.chains.llm import LLMChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

from ai_text_demo.utils import relative_path_from_file

DATA_PATH = relative_path_from_file(__file__, "data/state_of_the_union.txt")

# Load OPENAI_API_KEY
dotenv.load_dotenv()

# 1. Load
loader = TextLoader(DATA_PATH)
documents = loader.load()

# 2. Split
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(documents)

# 3. Store
vectorstore = Chroma.from_documents(documents, OpenAIEmbeddings())

# 4. Retrieve
retriever = vectorstore.as_retriever()

# 5.+6. Generate + Chat
print("Memory object to track chat history")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
llm = OpenAI(temperature=0)
qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, memory=memory)

query = "What did the president say about Ketanji Brown Jackson"
result = qa({"question": query})
print(result["answer"])

query = "Did he mention who she succeeded"
result = qa({"question": query})
print(result["answer"])

print("Pass in chat history explicitly")
qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever)

chat_history = []

query = "What did the president say about Ketanji Brown Jackson"
result = qa({"question": query, "chat_history": chat_history})
print(result["answer"])

query = "Did he mention who she succeeded"

print("Without chat history")
result = qa({"question": query, "chat_history": chat_history})
print(result["answer"])

print("With chat history")
chat_history = [(query, result["answer"])]
result = qa({"question": query, "chat_history": chat_history})
print(result["answer"])

print("Using a different model for condensing the question")
# By default, ChatOpenAI uses 'gpt-3.5-turbo'.
qa = ConversationalRetrievalChain.from_llm(
    # Use a more expensive model for answering the question.
    llm=ChatOpenAI(temperature=0, model="gpt-4"),
    retriever=retriever,
    # Use a cheaper and faster model for the simpler task of condensing the question
    # The condensation does not happen when the chat history is empty.
    condense_question_llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
)

chat_history = []
query = "What did the president say about Ketanji Brown Jackson"
result = qa({"question": query, "chat_history": chat_history})
print(result["answer"])

chat_history = [(query, result["answer"])]
query = "Did he mention who she succeeded"
result = qa({"question": query, "chat_history": chat_history})
print(result["answer"])

print("Using a custom prompt for condensing the question")
custom_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question. At the end of standalone question add this 'Answer the question in German language.' If you do not know the answer reply with 'I am sorry'.
Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CUSTOM_QUESTION_PROMPT = PromptTemplate.from_template(custom_template)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
qa = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(temperature=0),
    retriever=retriever,
    condense_question_prompt=CUSTOM_QUESTION_PROMPT,
    memory=memory
)

query = "What did the president say about Ketanji Brown Jackson"
result = qa({"question": query})
print(result["answer"])

query = "Did he mention who she succeeded"
result = qa({"question": query})
print(result["answer"])

print("Return Source Documents")
qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

chat_history = []
query = "What did the president say about Ketanji Brown Jackson"
result = qa({"question": query, "chat_history": chat_history})
print(result['source_documents'][0])

print("ConversationalRetrievalChain with `search_distance` threshold")
qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever
)

chat_history = []
query = "What did the president say about Ketanji Brown Jackson"
result = qa({"question": query, "chat_history": chat_history, "vectordbkwargs": {"search_distance": 0.9}})
print(result["answer"])

print("ConversationalRetrievalChain with `map_reduce`")
# The default chain_type is 'stuff'.
question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
doc_chain = load_qa_chain(llm, chain_type="map_reduce")

qa = ConversationalRetrievalChain(
    retriever=retriever,
    question_generator=question_generator,
    combine_docs_chain=doc_chain,
)

chat_history = []
query = "What did the president say about Ketanji Brown Jackson"
result = qa({"question": query, "chat_history": chat_history})
print(result["answer"])

print("ConversationalRetrievalChain with Question Answering with sources")
# Like the above, but appends sources at the end of the answer.
doc_chain = load_qa_with_sources_chain(llm, chain_type="map_reduce")

qa = ConversationalRetrievalChain(
    retriever=retriever,
    question_generator=question_generator,
    combine_docs_chain=doc_chain,
)

chat_history = []
query = "What did the president say about Ketanji Brown Jackson"
result = qa({"question": query, "chat_history": chat_history})
print(result["answer"])

print("ConversationalRetrievalChain with streaming to `stdout`")
# Construct a ConversationalRetrievalChain with a streaming llm for combine docs
# and a separate, non-streaming llm for question generation.
streaming_llm = OpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0)
doc_chain = load_qa_chain(streaming_llm, chain_type="stuff", prompt=QA_PROMPT)

qa = ConversationalRetrievalChain(
    retriever=retriever,
    question_generator=question_generator,
    combine_docs_chain=doc_chain,
)

chat_history = []
query = "What did the president say about Ketanji Brown Jackson"
qa({"question": query, "chat_history": chat_history})

chat_history = [(query, result["answer"])]
query = "Did he mention who she succeeded"
qa({"question": query, "chat_history": chat_history})
print()

print("get_chat_history Function")


# The default is "Human:{human}\nAssistant:{ai}".
def get_chat_history(inputs: list[tuple[str, str]]) -> str:
    res = []
    for human, ai in inputs:
        res.append(f"Human:{human}\nAI:{ai}")
    return "\n".join(res)


qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    get_chat_history=get_chat_history,
    verbose=True,
)

chat_history = []
query = "What did the president say about Ketanji Brown Jackson"
result = qa({"question": query, "chat_history": chat_history})
print(result["answer"])

chat_history = [(query, result["answer"])]
query = "Did he mention who she succeeded"
result = qa({"question": query, "chat_history": chat_history})
print(result["answer"])
