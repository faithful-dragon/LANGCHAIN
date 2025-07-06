import dotenv
from langchain_core.tools import Tool
from langchain.chat_models import init_chat_model
from langchain.agents import initialize_agent, AgentType

# Load env variables (e.g., OPENAI_API_KEY)
dotenv.load_dotenv()

# Constants
OPENAI_MODEL = "gpt-4o-mini"
MODEL_PROVIDER = "openai"

# ========== TOOL 1: Multiply ==========
def multiply_numbers(a: int, b: int) -> int:
    return a * b

def safe_multiply_tool(input_str: str) -> int:
    cleaned = input_str.replace("'", "").replace('"', "").strip()
    parts = cleaned.split()
    if len(parts) != 2:
        raise ValueError("Expected two numbers like: '3 4'")
    a, b = map(int, parts)
    return multiply_numbers(a, b)

multiply_tool = Tool(
    name="MultiplyTool",
    func=safe_multiply_tool,
    description="Multiplies two numbers. Input format: '3 4'"
)

# ========== TOOL 2: Add 100 ==========
def add_100_tool_func(input_str: str) -> int:
    cleaned = input_str.replace("'", "").replace('"', "").strip()
    num = int(cleaned)
    return num + 100

add_tool = Tool(
    name="Add100Tool",
    func=add_100_tool_func,
    description="Adds 100 to a given number. Input format: '30'"
)

# ========== Initialize LLM ==========
llm = init_chat_model(model=OPENAI_MODEL, model_provider=MODEL_PROVIDER)

# ========== Agent 1 (Multiplication Agent) ==========
agent1 = initialize_agent(
    tools=[multiply_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# ========== Agent 2 (Add 100 Agent) ==========
agent2 = initialize_agent(
    tools=[add_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# ========== Run Agents in Sequence ==========
# Agent 1: Multiply 5 and 6
response1 = agent1.invoke("What is 5 times 6?")
print("🧮 Agent 1 Result (Multiplication):", response1)

# Agent 2: Add 100 to result from Agent 1
# Extract numeric value from response1
import re
match = re.search(r"\b\d+\b", str(response1))
if match:
    value_from_agent1 = match.group()
    response2 = agent2.invoke(f"Add 100 to {value_from_agent1}")
    print("➕ Agent 2 Result (Add 100):", response2)
else:
    print("⚠️ Could not extract numeric result from Agent 1 response.")
