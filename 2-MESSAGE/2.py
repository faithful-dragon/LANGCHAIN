import os
import dotenv
import getpass
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

dotenv.load_dotenv()

# constants
OPENAI_MODEL = "gpt-4o-mini"
MODEL_PROVIDER = "openai"

# intialize chat model 
model = init_chat_model(model=OPENAI_MODEL, model_provider=MODEL_PROVIDER)

# example - 2
messages = [
    SystemMessage(content="You are a helpful assistant! Your name is Don and you are very good in writing short poems."),
    HumanMessage(content="Hi! I'm John"),
    AIMessage(content="Hello John! How can I assist you today?"),
    HumanMessage(content="What's my name and what's your name, also can you write 4 line short poem using our names?"),
]

# invoke model
response = model.invoke(messages)

# print all messages
# print(response)

# print exact model response
print(response.content)