import os
import dotenv
import helper as H
import data as D
dotenv.load_dotenv()

OPENAI_MODEL = "gpt-4o-mini"
MODEL_PROVIDER = "openai"
SYSTEM_MESSAGE = H.SystemMessage()
HUMAN_MESSAGE = H.HumanMessageFromDF(
    D.true_df,
    D.test_df
)