# import database as DB
# from langchain_core.tools import tool
from langchain.agents import initialize_agent, AgentType

# @tool
# def ConnectToDB():
#     """ use this tool if, connection to database is needed """
#     db = DB.GetDBConnection()
#     if db:
#         return "✅ Database connection successful!"
#     else:
#         return "❌ Database connection failed!"
   

def InitializeAgent(toolkit, llm):
    agent = initialize_agent(
        tools=toolkit.get_tools(),
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    return agent
