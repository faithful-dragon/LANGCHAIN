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

HUMAN_MESSAGE = "Give me a full JSON summary of the database schema. If there is any error, print that..!"

# Define messages
messages = prompt.format(system_message=H.system_message(), human_message=HUMAN_MESSAGE)

# ========== Initialize LLM and DB ==========
llm = init_chat_model(model=C.OPENAI_MODEL, model_provider=C.MODEL_PROVIDER)
db = DB.GetDBConnection()

# ========== Initialize Database Toolkit ==========
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# ========== Create Schema Agent ==========
dbConnectAgent = T.InitializeAgent(toolkit, llm)

# ========== Ask for schema summary ==========
response = dbConnectAgent.invoke(messages)
print(response)
