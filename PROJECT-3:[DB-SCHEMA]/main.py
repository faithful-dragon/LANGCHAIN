import dotenv
import tools as T
import helper as H
import constant as C
import database as DB
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.exceptions import OutputParserException
from openai import AuthenticationError, RateLimitError, APIError, Timeout
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

dotenv.load_dotenv()

# Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "{system_message}"),
    ("user", "{human_message}")
])

# ========== Prepare messages ==========
messages = prompt.format(
    system_message=C.SYSTEM_MESSAGE[0],
    human_message=C.HUMAN_MESSAGE[0]
)

# ========== Initialize LLM ==========
llm = init_chat_model(model=C.OPENAI_MODEL, model_provider=C.MODEL_PROVIDER)

# ========== Initialize Tools ==========
C.TOOLS.append(T.ConnectToDB)

# ========== Create Connection Agent ==========
dbConnectAgent = T.InitializeAgent(C.TOOLS, llm)

# ========== Ask Agent to Connect to DB ==========
try:
    response = dbConnectAgent.invoke(messages)
    print("✅ Agent response:", response)

    # Extract connection status from output
    output = response.get("output", "")
    connection_status = output.split('\n')[0]

    if connection_status:
        # ========== Initialize DB ==========
        db = DB.GetDBConnection()
        if db is None:
            raise Exception("🔴 DB returned None even though agent said connection was successful.")

        # ========== Initialize Toolkit ==========
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)

        # ========== Create Schema Agent ==========
        schemaAgent = T.InitializeAgent(toolkit.get_tools(), llm)

        # ========== Ask for schema summary ==========
        messages = prompt.format(
            system_message=C.SYSTEM_MESSAGE[1],
            human_message=C.HUMAN_MESSAGE[1]
        )

        schema_response = schemaAgent.invoke(messages)
        print("✅ Schema summary:\n", schema_response['output'])

    else:
        print("🔴 Database connection failed as per agent response.")

except OutputParserException as e:
    print("⚠️ Output format was not as expected:", e)

except AuthenticationError as e:
    print("🔒 OpenAI Authentication failed. Check your API key.")
    print("Details:", e)

except (RateLimitError, APIError, Timeout) as e:
    print("🚫 OpenAI API failed due to a rate limit or server error.")
    print("Details:", e)

except Exception as e:
    print("🔥 Unhandled exception occurred:")
    print(str(e))
