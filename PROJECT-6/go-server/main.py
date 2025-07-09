import io
import os
import dotenv
import helper as H
import pandas as pd
from langchain.chat_models import init_chat_model
from openai import OpenAIError, AuthenticationError
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.exceptions import OutputParserException

dotenv.load_dotenv()

OPENAI_MODEL = "gpt-4o-mini"
MODEL_PROVIDER = "openai"


def compare_translations(true_csv_path : str, test_csv_path : str, output_csv_path : str) -> pd.DataFrame:

    # Read input CSV files
    true_df = pd.read_csv(true_csv_path)
    test_df = pd.read_csv(test_csv_path)

    # Prepare messages
    system_message = H.SystemMessage()
    human_message = H.HumanMessageFromDF(true_df, test_df)

    # LangChain ChatPromptTemplate
    prompt = ChatPromptTemplate.from_messages([
        ("system", "{system_message}"),
        ("user", "{human_message}")
    ])
    messages = prompt.format(system_message=system_message, human_message=human_message)

    # Initialize LLM
    llm = init_chat_model(model=OPENAI_MODEL, model_provider=MODEL_PROVIDER)

    try:
        response = llm.invoke(messages)
        response_text = response.content.strip()

        if not response_text:
            raise ValueError("LLM response was empty")

        # Clean and parse CSV from LLM response
        cleaned_response = "\n".join(
            ",".join(col.strip() for col in line.split(","))
            for line in response_text.splitlines()
        )

        df_output = pd.read_csv(io.StringIO(cleaned_response))

        # Write to output CSV
        df_output.to_csv(output_csv_path, index=False)
        print(f"Output written to: {os.path.abspath(output_csv_path)}")
        return os.path.abspath(output_csv_path)

    except OutputParserException as e:
        print("⚠️ Output format was not as expected:", e)
        raise

    except AuthenticationError as e:
        print("🔒 OpenAI Authentication failed. Check your API key.")
        raise

    except OpenAIError as e:
        print("🚫 OpenAI API failed:", e)
        raise

    except Exception as e:
        print("🔥 Unhandled exception occurred:", str(e))
        raise


# Example usage (optional):
# Add to the bottom of your existing main.py
import sys

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py <true_csv> <test_csv> <output_csv>")
        sys.exit(1)

    true_csv_path = sys.argv[1]
    test_csv_path = sys.argv[2]
    output_csv_path = sys.argv[3]

    compare_translations(true_csv_path, test_csv_path, output_csv_path)

