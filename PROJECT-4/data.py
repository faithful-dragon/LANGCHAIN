import pandas as pd

# Example English and Spanish words
english = ["Hi", "Who", "Are", "Yes", "What", "You", "Your", "Place", "Pawan"]
spanish = ["Hola", "Quién", "Eres", "Sí", "Qué", "Tú", "Tu", "Lugar", "Pawan"]
french = ["Salut", "Qui", "Es", "Oui", "Quoi", "Toi", "Ton", "Lieu", "Pawan"]
german = ["Hallo", "Wer", "Bist", "Ja", "Was", "Du", "Dein", "Ort", "Pawan"]
hindi = ["नमस्ते", "कौन", "हो", "हाँ", "क्या", "तुम", "तुम्हारा", "स्थान", "पवन"]
thai = ["สวัสดี", "ใคร", "คือ", "ใช่", "อะไร", "คุณ", "ของคุณ", "สถานที่", "พาวัน"]

# Create DataFrames
english_df = pd.DataFrame({"s.no": [1, 2, 3, 4, 5, 6, 7, 8, 9], "english": english})
spanish_df = pd.DataFrame({"s.no": [1, 2, 3, 4, 5, 6, 7, 8, 9], "spanish": spanish})
french_df = pd.DataFrame({"s.no": [1, 2, 3, 4, 5, 6, 7, 8, 9], "french": french})
german_df = pd.DataFrame({"s.no": [1, 2, 3, 4, 5, 6, 7, 8, 9], "german": german})
hindi_df = pd.DataFrame({"s.no": [1, 2, 3, 4, 5, 6, 7, 8, 9], "hindi": hindi})
thai_df = pd.DataFrame({"s.no": [1, 2, 3, 4, 5, 6, 7, 8, 9], "thai": thai})

print("✅ Data loaded.")