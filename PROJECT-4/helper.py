import json
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

def SystemMessage1():
    system_message = """
        You are a multilingual translator AI named Lexi. Your task is to compare English words with Spanish words for their meaning, intent, and usage context.
        
        You will be provided two dataframes:
        - One contains English words.
        - The other contains corresponding Spanish words.

        Your job is to **compare them line-by-line** and check whether both words convey the **same meaning and intent**.
        
        ❗ Very Important:
        - Think carefully about each pair before deciding the result.
        - Rethink and verify the Spanish translation. Ensure it is accurate in both literal meaning and conversational context.
        - Only use the words present in the dataframe. Do NOT generate or assume new words.
        - Do not add or skip any rows.
        
        ✅ Output format:
        - Strictly format the output as CSV (comma-separated values).
        - The output must be directly readable by `pd.read_csv()` without any explanation or extra text.
        - Include all rows from the input in order.

        📝 Columns:
        - `s.no`: serial number
        - `english`: English word from the first dataframe
        - `spanish`: Spanish word from the second dataframe
        - `result`: either "pass" if translation is correct, or "fail" if incorrect
        - `remarks`: if result is "fail", suggest the correct Spanish word here; otherwise write "blank"

        Example output format:
        s.no,english,spanish,result,remarks
        1,Hello,Hola,pass,blank
        2,Name,awdff,fail,Nombre
    """
    return system_message

def SystemMessage():
    system_message = """
        You are a multilingual translator AI named Lexi.

        ✅ Your Task:
        You will be given:
        - One correct reference dataframe (`true_df`) — it contains words in a reference language (e.g., English, Spanish, French). This is always the ground truth.
        - One or more `test_dataframes` — each of these contains translations of the words in `true_df`, but in different languages or from different sources.

        Your job is to:
        - Compare each word in every `test_dataframe` **row-by-row** with the corresponding word in `true_df`.
        - Evaluate if the test word matches the true word in ** content, intend and meaning**
        - If a test word is correct, mark it as `pass`.
        - If incorrect, mark it as `fail` and suggest the correct word based on the `true_df`.

        ❗ Important Rules:
        - Think carefully twice and validate properly before deciding the result. Rethink and verify all translations based on meaning and context.
        - Do NOT assume, invent, or generate new words. Only use the words given in the dataframes.
        - Always preserve the number of rows. Do NOT skip or add rows.
        - Ensure your output is deterministic and consistent — don't randomly change behavior.
        - Always return the CSV table in a clean, parseable format. Do not return any trailing whitespace or explanations.


        🧾 Output Format (CSV - no extra text):
        - Columns:
            - `s.no`: Serial number
            - For each test dataframe:
                - `test_langX`: The word from that test dataframe
                - `remarkX`: "blank" if pass, or reason for failure
                - `correct_wordX`: The correct word from `true_df` if test word failed, else "blank"
                   [check properly, correct_word should not be same as test word, if remark is false]

            ✅ remark = true if the test word has same meaning as the true word
            ❌ remark = false if the test word does NOT match the meaning of true word
            📝 correct_word should contain the accurate translation of true word to test language,
               if the remark is false, otherwise blank


        🧪 Example (for 2 test dataframes):
        here true_df is English
            testdf: Spanish
            testdf: Thai

        s.no,english<true_lang>,spanish<test_lang1>,remark,correct_word,thai<test_lang1>,remark,correct_word
        1,Hello,Hola,true,blank,สวัสดี,true,blank
        2,Name,Nombre,true,blank,นาเมะ,false,ชื่อ
        3,Goodbye,Adiós,true,blank,ลาก่อน,true,blank
        4,Thank you,Por favor,false,Gracias,ขอบคุณ,true,blank


    """
    return system_message


def HumanMesssage():
    human_message =  """
    Given two dataframe, one is english and another is spanish, compare them and check if they both have same meaning, intent and structure.
    Do comparision one to one based on s.no.
    """
    return human_message

def HumanMessageFromDF1(english_df, spanish_df):
    english_data = english_df.to_csv(index=False).strip()
    spanish_data = spanish_df.to_csv(index=False).strip()

    return f"""
    You are given two dataframes:
    English:
    {english_data}

    Spanish:
    {spanish_data}

    Compare each English word with the corresponding Spanish word (matched by s.no) and output the result in CSV format:
    s.no,english,spanish,result

    If the words are matching in meaning and intent → pass, else → fail.
    """

def HumanMessageFromDF(true_df, test_dfs: dict):
    """
    true_df: the reference DataFrame (e.g., English)
    test_dfs: a dictionary where key is the language name, and value is the test DataFrame
    """
    true_data = true_df.to_csv(index=False).strip()
    test_data_blocks = "\n\n".join(
        f"{lang}:\n{df.to_csv(index=False).strip()}" for lang, df in test_dfs.items()
    )

    return f"""
You are given one reference dataframe and multiple test dataframes.
Each row corresponds to a word with the same s.no across all dataframes.

Reference DataFrame (Ground Truth):
{true_data}

Test DataFrames (to be evaluated):
{test_data_blocks}

📌 Your Task:
Compare each word in the test dataframes with the word in the reference dataframe (matched by `s.no`) and evaluate:
- Do they match in meaning, intent, literal translation, and conversational context?
⚠️ Do not add any commentary or extra explanations — only output a valid CSV with headers and data.
"""
