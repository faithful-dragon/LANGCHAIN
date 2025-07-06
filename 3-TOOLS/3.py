import os
import dotenv
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Load environment variables
dotenv.load_dotenv()

# Constants
OPENAI_MODEL = "gpt-4o-mini"
MODEL_PROVIDER = "openai"
SYSTEM_MESSAGE = []
HUMAN_MESSAGE = []
TOOLS = []

# Define structured output format using Pydantic
class ResponseFormatter1(BaseModel):
    """Always use this tool to structure your response to the user."""
    question: str = Field(description="The user's individal question present in prompt")
    logic: str = Field(description="The logic used to answer the prompt")
    tool_calls: str = Field(description="List of tool calls done by model to answer the prompt")
    answer: str = Field(description="The answer to the user's question")
    followup_question: str = Field(description="A followup question the user could ask")

# Define a tool for multiplication
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

# Add tools to the list
TOOLS.append(multiply_two_num)
TOOLS.append(add_two_num)
TOOLS.append(subtract_two_num)

# Initialize chat model
def init_model_with_tools(tools):
    model = init_chat_model(model=OPENAI_MODEL, model_provider=MODEL_PROVIDER)
    model_with_tools = model.bind_tools(tools)
    return model_with_tools

model = init_model_with_tools(TOOLS)

# Wrap model with structured output schema
structured_llm = model.with_structured_output(ResponseFormatter1)

# Custom system message to enforce the output structure
def system_message():
    return [
        """
        You are a maths teacher name Pawan and must solve problems using the available tools.

        Always structure your response using this format:
        - question: The exact question(s) the user asked.
        - logic: Mention your name and then Step-by-step reasoning used to solve it.
        - tool_calls: Mention any tool names used (e.g., multiply_two_num, add_two_num) and inputs.
        - answer: The final numeric result(s).
        - followup_question: A natural follow-up related to the question.
        """,
        """
        You are a biology teacher, name Ankita and must solve problems using the available tools.

        Always structure your response using this format:
        - question: The exact question(s) the user asked.
        - logic: Mention your name and then Step-by-step reasoning used to solve it.
        - tool_calls: Mention any tool names used (e.g., multiply_two_num, add_two_num) and inputs.
        - answer: The final numeric result(s).
        - followup_question: A natural follow-up related to the question.
        """
    ]

def human_message():
    return [
        "What is the powerhouse of the cell?",
        "Multiply 2 by 3?",
        '''
            Solve below maths problem: 
            Q1: 2 + 3 = ?,
            Q2: 4 * 5 = ?,
            Q3: 6 - 7 = ?,
            Q4: 8 / 9 = ?
        ''',
        "Explain the process of Photosynthesis."
    ]

SYSTEM_MESSAGE = system_message()
HUMAN_MESSAGE = human_message()

# Define prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "{system_message}"),
    ("user", "{human_message}")
])

# Define messages
messages1 = prompt.format(system_message=SYSTEM_MESSAGE[1], human_message=HUMAN_MESSAGE[0])
messages2 = prompt.format(system_message=SYSTEM_MESSAGE[0], human_message=HUMAN_MESSAGE[1])
messages3 = prompt.format(system_message=SYSTEM_MESSAGE[0], human_message=HUMAN_MESSAGE[2])
messages4 = prompt.format(system_message=SYSTEM_MESSAGE[1], human_message=HUMAN_MESSAGE[3])


# Invoke messages
def run_prompt(messages, label=""):
    print(f"\n--- {label} ---")

    # Get structured output
    structured_response = structured_llm.invoke(messages)

    # Print structured content
    print("Question:", structured_response.question)
    print("Logic:", structured_response.logic)
    print("Tool Calls:", structured_response.tool_calls)
    print("Answer:", structured_response.answer)
    print("Followup Question:", structured_response.followup_question)
    print()

# Run both prompts
run_prompt(messages1, label="Test 1: Biology Question")
run_prompt(messages2, label="Test 2: Math Tool Question")
run_prompt(messages3, label="Test 3: Multiple Math Tool Question")
run_prompt(messages4, label="Test 4: Biology Question")
