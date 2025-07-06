import dotenv
from langchain_core.tools import Tool
from langchain.chat_models import init_chat_model
from langchain.agents import initialize_agent, AgentType

# Load environment variables (e.g., OPENAI_API_KEY)
dotenv.load_dotenv()

# Constants
OPENAI_MODEL = "gpt-4o-mini"
MODEL_PROVIDER = "openai"

# Tool: Multiplies two numbers
def multiply_numbers(a: int, b: int) -> int:
    return a * b

def safe_multiply_tool(input_str: str) -> int:
    # Clean quotes and ensure input is two integers
    cleaned = input_str.replace("'", "").replace('"', "").strip()
    parts = cleaned.split()
    if len(parts) != 2:
        raise ValueError("Expected two numbers like: '3 4'")
    a, b = map(int, parts)
    return multiply_numbers(a, b)

# Define the tool
calculator_tool = Tool(
    name="MultiplyTool",
    func=safe_multiply_tool,
    description="Multiplies two numbers. Input format: '3 4'"
)

# Initialize chat model
llm = init_chat_model(
    model=OPENAI_MODEL,
    model_provider=MODEL_PROVIDER
)

# Initialize the agent with the tool
agent = initialize_agent(
    tools=[calculator_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Use agent.invoke() instead of deprecated agent.run()
response = agent.invoke("What is 5 times 6?")
print("✅ Result:", response)
