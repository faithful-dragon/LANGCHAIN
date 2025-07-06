import os
import dotenv
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableMap, RunnablePassthrough

# Load environment variables
dotenv.load_dotenv()

# Constants
OPENAI_MODEL = "gpt-4o-mini"
MODEL_PROVIDER = "openai"

# Pydantic response schema
class ResponseFormatter1(BaseModel):
    question: str = Field(description="The user's individual question present in prompt")
    logic: str = Field(description="The logic used to answer the prompt")
    tool_calls: str = Field(description="List of tool calls done by model to answer the prompt")
    answer: str = Field(description="The answer to the user's question")
    followup_question: str = Field(description="A follow-up question the user could ask")

# Tools
@tool
def multiply_two_num(a: int, b: int) -> int:
    """Use when you need to multiply two numbers."""
    return a * b

@tool
def add_two_num(a: int, b: int) -> int:
    """Use when you need to add two numbers."""
    return a + b

@tool
def subtract_two_num(a: int, b: int) -> int:
    """Use when you need to subtract two numbers."""
    return a - b

# Tool list
TOOLS = [multiply_two_num, add_two_num, subtract_two_num]

# Init model with tools
def init_model_with_tools(tools):
    model = init_chat_model(model=OPENAI_MODEL, model_provider=MODEL_PROVIDER)
    return model.bind_tools(tools)

model = init_model_with_tools(TOOLS)
structured_llm = model.with_structured_output(ResponseFormatter1)

# System messages
def system_message():
    return """
        Your name is Alexender and you are virtual assistant.
        Always structure your response using this format:
        - question: The exact question(s) the user asked.
        - logic: Mention your name and then Step-by-step reasoning used to solve it.
        - tool_calls: Mention any tool names used (e.g., multiply_two_num, add_two_num) and inputs.
        - answer: The final numeric result(s).
        - followup_question: A natural follow-up related to the question.
        """
    

# Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "{system_message}"),
    ("user", "{human_message}")
])

# Runnable Chain
chain = (
    RunnableMap({
        "system_message": lambda x: x["system_message"],
        "human_message": lambda x: x["human_message"]
    })
    | prompt
    | structured_llm
)

# Run chain on examples
def run_chain(user_input):
    response = chain.invoke({
        "system_message": system_message(),
        "human_message": user_input
    })
    print("Question:", response.question)
    print("Logic:", response.logic)
    print("Tool Calls:", response.tool_calls)
    print("Answer:", response.answer)
    print("Followup Question:", response.followup_question)
    print()

def main():
    print("Hi! I'm your virtual assistant. How can I help you today? [Enter 'quit' to exit]")
    while True:
        user_input = input("You: ")
        if user_input == "quit":
            break
        else:
            run_chain(user_input)
    print("Goodbye!")

if __name__ == "__main__":
    main()