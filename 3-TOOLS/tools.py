import dotenv
from langchain_core.tools import tool

dotenv.load_dotenv()
# Tools implement the Runnable interface, which means that they can be invoked (e.g., tool.invoke(args)) directly.
# creating tool using function
@tool
def multiply(a: int, b: int) -> int:
   """Multiply two numbers."""
   return a * b

print(multiply.invoke({"a": 2, "b": 3}))
print(multiply.name)
print(multiply.description)
print(multiply.args)
print()

from typing import Annotated, List

# Note that @tool supports parsing of annotations, nested schemas, and other features:
@tool
def multiply_by_max(
    a: Annotated[int, "scale factor"],
    b: Annotated[List[int], "list of ints over which to take maximum"],
) -> int:
    """Multiply a by the maximum of b."""
    return a * max(b)

print(multiply_by_max.args_schema.model_json_schema())
print()


# You can also customize the tool name and JSON args by passing them into the tool decorator.
from pydantic import BaseModel, Field
class CalculatorInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")


@tool("multiplication-tool", args_schema=CalculatorInput, return_direct=True)
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

# Let's inspect some of the attributes associated with the tool.
print(multiply.name)
print(multiply.description)
print(multiply.args)
print(multiply.return_direct)
print()

# structured_tool
from langchain_core.tools import StructuredTool

def multiply1(a: int, b: int) -> int:
   """Multiply two numbers."""
   return a * b

calculator = StructuredTool.from_function(
    func=multiply1,
    name="Calculator",
    description="multiply numbers",
    args_schema=CalculatorInput,
    return_direct=True,
    # coroutine= ... <- you can specify an async method if desired as well
)

print(calculator.name)
print(calculator.description)
print(calculator.args)
print(calculator.return_direct)
print(calculator.invoke({"a": 2, "b": 3}))
print()