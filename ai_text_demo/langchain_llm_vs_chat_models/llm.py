import dotenv
from langchain.llms import OpenAI
from langchain.schema import SystemMessage, HumanMessage

# Load OPENAI_API_KEY
dotenv.load_dotenv()

llm = OpenAI()

# __call__
print(llm("Tell me a joke"))

# generate
llm_result = llm.generate(["Tell me a joke", "Tell me a poem"]*15)
print(len(llm_result.generations))
print(llm_result.generations[0])
print(llm_result.generations[-1])
print(llm_result.llm_output)

print("Base Language Model interface")
print(llm.predict("Tell me a joke"))
messages = [
    SystemMessage(content="You are a helpful assistant that translates English to French."),
    HumanMessage(content="I love programming.")
]
print(llm.predict_messages(messages))
