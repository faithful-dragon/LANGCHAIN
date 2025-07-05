# LLM -> OPENAI

import dotenv
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # api_key="...",
    # base_url="...",
    # organization="...",
    # other params...
)

messages = [
    (
        "system",
        "You are a helpful translator. Translate the user sentence to French.",
    ),
    ("human", "I love programming."),
]

response = llm.invoke(messages)
print(response.content)