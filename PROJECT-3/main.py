import dotenv
import tools as T
import helper as H
import constant as C
import database as DB
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.chat_models import init_chat_model

dotenv.load_dotenv()

# Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "{system_message}"),
    ("user", "{human_message}")
])

# Define messages
messages = prompt.format(system_message=C.SYSTEM_MESSAGE[0], human_message=C.HUMAN_MESSAGE[0])

# ========== Initialize LLM ==========
llm = init_chat_model(model=C.OPENAI_MODEL, model_provider=C.MODEL_PROVIDER)

# ========== Initialize Tools ==========
C.TOOLS.append(T.ConnectToDB)

# ========== Create Schema Agent ==========
dbConnectAgent = T.InitializeAgent(C.TOOLS, llm)

# ========== Ask for schema summary ==========
response = dbConnectAgent.invoke(messages)
print(response)
print(response['output'])

connnection_response = response['output'].split('\n')[0]
if connnection_response:

    # ========== Initialize Database Toolkit ==========
    db = DB.GetDBConnection()
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # ========== Create Schema Agent ==========
    schemaAgent = T.InitializeAgent(toolkit.get_tools(), llm)

    # ========== Ask for schema summary ==========
    messages = prompt.format(system_message=C.SYSTEM_MESSAGE[1], human_message=C.HUMAN_MESSAGE[1])

    schema_summary = schemaAgent.invoke(messages)
    print(schema_summary)