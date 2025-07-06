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
    return [
        """You are a maths teacher named Pawan and must solve problems using the available tools.

        Always structure your response using this format:
        - question: The exact question(s) the user asked.
        - logic: Mention your name and then Step-by-step reasoning used to solve it.
        - tool_calls: Mention any tool names used (e.g., multiply_two_num, add_two_num) and inputs.
        - answer: The final numeric result(s).
        - followup_question: A natural follow-up related to the question.
        """,
        """You are a biology teacher named Ankita and must solve problems using the available tools.

        Always structure your response using this format:
        - question: The exact question(s) the user asked.
        - logic: Mention your name and then Step-by-step reasoning used to solve it.
        - tool_calls: Mention any tool names used (e.g., multiply_two_num, add_two_num) and inputs.
        - answer: The final numeric result(s).
        - followup_question: A natural follow-up related to the question.
        """
    ]

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

# Sample inputs
examples = [
    {
        "label": "Test 1: Biology Question",
        "system_message": system_message()[1],
        "human_message": "What is the powerhouse of the cell?"
    },
    {
        "label": "Test 2: Math Tool Question",
        "system_message": system_message()[0],
        "human_message": "Multiply 2 by 3?"
    },
    {
        "label": "Test 3: Multiple Math Tool Question",
        "system_message": system_message()[0],
        "human_message": '''
            Solve below maths problem: 
            Q1: 2 + 3 = ?,
            Q2: 4 * 5 = ?,
            Q3: 6 - 7 = ?,
            Q4: 8 / 9 = ?
        '''
    },
    {
        "label": "Test 4: Biology Question",
        "system_message": system_message()[1],
        "human_message": "Explain the process of Photosynthesis."
    },
]

# Run chain on examples
def run_chain(chain, example):
    print(f"\n--- {example['label']} ---")
    response = chain.invoke(example)
    print("Question:", response.question)
    print("Logic:", response.logic)
    print("Tool Calls:", response.tool_calls)
    print("Answer:", response.answer)
    print("Followup Question:", response.followup_question)

for example in examples:
    run_chain(chain, example)
