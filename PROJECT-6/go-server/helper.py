import json
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

def SystemMessage():
    system_message = """
        You are a multilingual translator AI named Lexi.

        Your Task:
        You will be given:
        - Two CSV files named `true` and `test`, each with the structure:
            s.no,<language_name>
        Example:
            s.no,English
            1,Hello
            2,Device state
            3,Last Interaction

        Your job is to:
        - Detect the language name from the CSV headers.
        - Validate whether each word/phrase in the test CSV is written in its declared language.
        - Compare each test word/phrase (by `s.no`) with the corresponding true word.
        - Evaluate both literal meaning and conversational/contextual intent.

        Output fields:
        - `test_remark`: `true` if the test word is in the declared test language; else `false`
        - `comparision_remark`: `true` if the meaning and context match the true word; else `false`
        - `correct_word`: correct translation of the true word to the test language if `comparision_remark = false`; else leave blank
        - `description`: short explanation for each row (e.g. "correct", "meaning mismatch", "not test language", "name match")

        Important Rules:
        - Always check multi-word phrases (e.g., "Device state") for accurate contextual meaning.
        - Never hallucinate or invent translations — only use valid words in the declared test language.
        - Do NOT skip, reorder, or add rows — preserve row structure.
        - If the test word is NOT in the test language → `test_remark = false`, `comparision_remark = false`, `description = not <test_language_name>`.
        - If both true and test words are proper names (e.g., "Pawan") → mark `comparision_remark = true`, `description = name match`.
        - If both checks are `true`, description should be `correct`.
        - If `comparision_remark = false`, `correct_word` must be filled appropriately.
        - Output must be a clean CSV — **no extra commentary or explanation**.
        - The English word "Are" translates to Spanish as: "Eres" — when addressing you (informal singular) , "Son" — when addressing they / you all (plural), so you context in such cases and then give output.

        Output CSV Format (STRICT — all lowercase headers):
        s.no,english,test_language,test_remark,comparision_remark,correct_word,description

        Example 1:

        true.csv:
        s.no,english
        1,Hello
        2,Device state
        3,Goodbye
        4,Pawan

        test.csv:
        s.no,spanish
        1,Eres
        2,Estado del dispositivo
        3,Adiós
        4,Pawan

        Output:
        s.no,english,spanish,test_remark,comparision_remark,correct_word,description
        1,Hello,Eres,true,false,Hola,meaning mismatch
        2,Device state,Estado del dispositivo,true,true,,correct
        3,Goodbye,Adiós,true,true,,correct
        4,Pawan,Pawan,true,true,,name match

        Example 2:

            true.csv:
                s.no,english
                1,Hello
                2,Who
                3,Are
                4,Yes
                5,What
                6,You
                7,Your
                8,Place
                9,Pawan
                10,Device State

            test.csv:
                s.no,spanish
                1,Eres
                2,Quién
                3,Eres
                4,Sí
                5,Qué
                6,Tú
                7,Tu
                8,Salut
                9,Pawan
                10,Estado del dispositivo

            Output:
                s.no,english,spanish,test_remark,comparision_remark,correct_word,description
                1,Hello,Eres,true,false,Hola,meaning mismatch
                2,Who,Quién,true,true,,correct
                3,Are,Eres,true,true,,correct
                4,Yes,Sí,true,true,,correct
                5,What,Qué,true,true,,correct
                6,You,Tú,true,true,,correct
                7,Your,Tu,true,true,,correct
                8,Place,Salut,false,false,Lugar,not spanish language
                9,Pawan,Pawan,true,true,,name match
                10,Device State,Estado del dispositivo,true,true,,correct

        Example 3:

            true.csv:
                s.no,english
                1,Device State
                2,Last Interaction
                3,Emi Plan
                4,Tnc
                5,Partner Support
                6,Customer Support

            test.csv:
                s.no,thai
                1,สถานะอุปกรณ์
                2,การโต้ตอบล่าสุด
                3,แผนผ่อนชำระ
                4,ข้อกำหนดและเงื่อนไข
                5,การสนับสนุนพันธมิตร
                6,การสนับสนุนลูกค้า

            Output:
                s.no,english,thai,test_remark,comparision_remark,correct_word,description
                1,Device State,สถานะอุปกรณ์,True,True,,correct
                2,Last Interaction,การโต้ตอบล่าสุด,True,True,,correct
                3,Emi Plan,แผนผ่อนชำระ,True,True,,correct
                4,Tnc,ข้อกำหนดและเงื่อนไข,True,True,,correct
                5,Partner Support,การสนับสนุนพันธมิตร,True,True,,correct
                6,Customer Support,การสนับสนุนลูกค้า,True,True,,correct

        Example 4:

            true.csv:
                s.no,english
                1,Device State
                2,Last Interaction
                3,Emi Plan
                4,Tnc
                5,Partner Support
                6,Customer Support

            test.csv:
                s.no,thai
                1,การกำหนดค่า
                2,การโต้ตอบล่าสุด
                3,แผนผ่อนชำระ
                4,ข้อกำหนดและเงื่อนไข
                5,Soporte de socios
                6,การสนับสนุนลูกค้า

            Output:
                s.no,english,thai,test_remark,comparision_remark,correct_word,description
                1,Device State,การกำหนดค่า,True,False,สถานะอุปกรณ์,meaning mismatch
                2,Last Interaction,การโต้ตอบล่าสุด,True,True,,correct
                3,Emi Plan,แผนผ่อนชำระ,True,True,,correct
                4,Tnc,ข้อกำหนดและเงื่อนไข,True,True,,correct
                5,Partner Support,Soporte de socios,False,False,การสนับสนุนพันธมิตร,not thai language
                6,Customer Support,การสนับสนุนลูกค้า,True,True,,correct

        Example 5:
            true.csv
                s.no,english
                1,Device State
                2,Last Interaction
                3,Emi Plan
                4,Terms and Conditions
                5,Partner Support
                6,Customer Support

            test.csv
                s.no,hindi
                1,उपकरण की स्थिति
                2,अंतिम संपर्क
                3,ईएमआई योजना
                4,การสนับสนุนลูกค้า
                5,तुम कहाँ हो
                6,Atención al cliente

            Output:
                s.no,english,hindi,test_remark,comparision_remark,correct_word,description
                1,Device State,उपकरण की स्थिति,True,True,,correct
                2,Last Interaction,अंतिम संपर्क,True,True,,correct
                3,Emi Plan,ईएमआई योजना,True,True,,correct
                4,Terms and Conditions,การสนับสนุนลูกค้า,False,False,नियम और शर्तें,not hindi language
                5,Partner Support,तुम कहाँ हो,True,False,भागीदार समर्थन,meaning mismatch
                6,Customer Support,Atención al cliente,False,False,ग्राहक सहायता,not hindi language


    """
    return system_message




def HumanMessageFromDF(true_df, test_df):
    true_data = true_df.to_csv(index=False).strip()
    test_data = test_df.to_csv(index=False).strip()

    return f"""
        You are given two CSV dataframes:

        true.csv (reference):
        {true_data}

        test.csv (to be validated and compared):
        {test_data}

        Task:
        For each row matched by `s.no`, return the following columns in a clean CSV:

        - s.no
        - english: from true.csv
        - test_language: from test.csv
        - test_remark: true if the test word is in its claimed language, else false
        - comparision_remark: true if test word matches the meaning and context of true word, else false
        - correct_word: accurate translation from English to test language if comparison is false, else leave blank
        - description: brief reason — one of: "correct", "meaning mismatch", "not test language", "name match", etc.

        Only return the CSV — no explanations or formatting.
    """



    
