import os
import dotenv
import getpass
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

dotenv.load_dotenv()

# constants
OPENAI_MODEL = "gpt-4o-mini"
MODEL_PROVIDER = "openai"

# intialize chat model 
model = init_chat_model(model=OPENAI_MODEL, model_provider=MODEL_PROVIDER)

# example - 1
messages = [
    SystemMessage(
        content="You are a helpful assistant! Your name is Bob."
    ),
    HumanMessage(
        content="What is your name?"
    )
]

# invoke model
response = model.invoke(messages)

# print all messages
# print(response)

# print exact model response
print(response.content)