import io
import os
import pandas as pd
import dotenv
import data as D
import constant as C
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.exceptions import OutputParserException
from openai import AuthenticationError, RateLimitError, APIError, Timeout

dotenv.load_dotenv()

# Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "{system_message}"),
    ("user", "{human_message}")
])

# ========== Prepare messages ==========
messages = prompt.format(
    system_message=C.SYSTEM_MESSAGE,
    human_message=C.HUMAN_MESSAGE
)
print("Messages prepared.")

# ========== Initialize LLM ==========
llm = init_chat_model(model=C.OPENAI_MODEL, model_provider=C.MODEL_PROVIDER)

try:
    response = llm.invoke(messages)

    # STEP 1: Extract text content
    response_text = response.content.strip()

    if not response_text:
        print("LLM response was empty!")
        exit(1)

    # Optional: Print for debugging
    print("Raw LLM Response:\n", response_text)

    # STEP 2: Clean and parse CSV
    cleaned_response = "\n".join(
        ",".join(col.strip() for col in line.split(","))
        for line in response_text.splitlines()
    )

    df_output = pd.read_csv(io.StringIO(cleaned_response))

    # STEP 3: Save the DataFrame to a CSV file
    output_path = "output_translations.csv"
    df_output.to_csv(output_path, index=False)

    print("DataFrame created and written to:", os.path.abspath(output_path))
    print(df_output.head())

except OutputParserException as e:
    print("Output format was not as expected:", e)

except AuthenticationError as e:
    print("OpenAI Authentication failed. Check your API key.")
    print("Details:", e)

except (RateLimitError, APIError, Timeout) as e:
    print("OpenAI API failed due to a rate limit or server error.")
    print("Details:", e)

except Exception as e:
    print("Unhandled exception occurred:")
    print(str(e))
