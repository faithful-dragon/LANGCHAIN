import os
import dotenv
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Load environment variables
dotenv.load_dotenv()

# Constants
OPENAI_MODEL = "gpt-4o-mini"
MODEL_PROVIDER = "openai"

# Define structured output format using Pydantic
class ResponseFormatter(BaseModel):
    """Always use this tool to structure your response to the user."""
    answer: str = Field(description="The answer to the user's question")
    followup_question: str = Field(description="A followup question the user could ask")

# Define a tool for multiplication
@tool
def multiply_two_num(a: int, b: int) -> int:
    """Use when you need to multiply two numbers."""
    return a * b

# Initialize chat model
model = init_chat_model(model=OPENAI_MODEL, model_provider=MODEL_PROVIDER)

# Bind tool
model_with_tools = model.bind_tools([multiply_two_num])

# Wrap model with structured output schema
structured_llm = model_with_tools.with_structured_output(ResponseFormatter)

# Define message examples
messages1 = [
    SystemMessage(content="You are a maths teacher and you are very efficient in answering mathematics questions."),
    HumanMessage(content="What is the powerhouse of the cell?"),
]

messages2 = [
    SystemMessage(content="You are a maths teacher and you are very efficient in answering mathematics questions."),
    HumanMessage(content="Multiply 2 by 3?"),
]

# Function to check if a tool was called
def check_tool_usage(ai_message: AIMessage):
    if hasattr(ai_message, "tool_calls") and ai_message.tool_calls:
        print("✅ Tool was called:", ai_message.tool_calls[0]['name'])
    else:
        print("❌ Tool was NOT called.")

# Invoke messages and capture both structured and raw responses
def run_prompt(messages, label=""):
    print(f"\n--- {label} ---")

    # Get structured output
    structured_response = structured_llm.invoke(messages)

    # Get raw message to check tool usage
    raw_response = model_with_tools.invoke(messages)
    check_tool_usage(raw_response)

    # Print structured content
    print("Answer:", structured_response.answer)
    print("Followup Question:", structured_response.followup_question)
    print(raw_response.tool_calls)
    print()

# Run both prompts
run_prompt(messages1, label="Test 1: Biology Question")
run_prompt(messages2, label="Test 2: Math Tool Question")
