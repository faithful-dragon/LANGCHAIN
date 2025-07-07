import database as DB
from typing import Optional
from langchain_core.tools import tool
from langchain.agents import initialize_agent, AgentType



@tool
def ConnectToDB(dummy_input: Optional[str] = None) -> str:
    """Use this tool if connection to the database is needed"""
    db = DB.GetDBConnection()
    if db:
        return "✅ Database connection successful!"
    else:
        return "❌ Database connection failed!"

   

def InitializeAgent(tools, llm):
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        max_iterations=3,  # ⛔️ prevent infinite loops
        verbose=True,
        early_stopping_method="generate"
    )
    return agent
