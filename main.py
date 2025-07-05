import os
import dotenv
from openai import OpenAI

dotenv.load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = OpenAI(
  api_key=OPENAI_API_KEY
)

completion = llm.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "List 20 countries name and their capital in json format."}
  ]
)

print(completion.choices[0].message)