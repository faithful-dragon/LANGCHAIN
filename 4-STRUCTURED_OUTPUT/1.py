import os
import dotenv
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables (e.g., your OpenAI API key)
dotenv.load_dotenv()

# Define the response format using Pydantic
class ResponseFormatter(BaseModel):
    """Always use this tool to structure your response to the user."""
    answer: str = Field(description="The answer to the user's question")
    followup_question: str = Field(description="A followup question the user could ask")


# Constants
OPENAI_MODEL = "gpt-4o-mini"
MODEL_PROVIDER = "openai"

# Initialize chat model
model = init_chat_model(model=OPENAI_MODEL, model_provider=MODEL_PROVIDER)

# Wrap the model to return structured output using the Pydantic schema
structured_llm = model.with_structured_output(ResponseFormatter)

# Define the chat messages
messages = [
    SystemMessage(content="You are a biology teacher and you are very efficient in answering biology questions."),
    HumanMessage(content="What is the powerhouse of the cell?"),
]

# Get structured response from the model
structured_response = structured_llm.invoke(messages)

# Print the results
print("Answer:", structured_response.answer)
print("Followup Question:", structured_response.followup_question)
