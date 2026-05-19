from openai import OpenAI
import json
from dotenv import load_dotenv
import os

load_dotenv()

client_openai = OpenAI(
    base_url=os.getenv("LLM_PORT"),
    api_key="lm-studio"
)

with open("1_python_ai_applied/files/Resenhas_App_ChatGPT.txt", "r", encoding="utf-8") as file:
    review = file.read()

review_lst = review.split("\n")
review_dct = dict()

for idx, review in enumerate(review_lst):
    llm_reponse = client_openai.chat.completions.create(
        model="google/gemma-3-1b",
        messages=[
            {
                "role": "system", 
                "content": """Você é um analista de resenhas de aplicativos.
                Sua tarefa é analisar as resenhas e identificar as informações de cada linha de informação.
                As linhas de informação são separadas por '$' e na sequência, as informações são o ID do usuário,
                o nome do usuário e a resenha em seu idioma original. O formato é ID_do_Usuario$Nome_do_Usuario$Resenha_Original."""
            },
            {
                "role": "user", 
                "content": f"""Retorne para mim o nome do usuário, a resenha original, 
                a resenha traduzida para o português e a avaliação de cada resenha. 
                A avaliação deve ser representada por uma única palavra 
                (Positiva, Negativa ou Neutra). Esses dados devem ser retornados em formato JSON. 
                
                Use o seguinte formato de JSON:
                {{
                    "Nome_do_Usuario": "<nome do usuário>",
                    "Resenha_Original": "<resenha original>",
                    "Resenha_Traduzida": "<resenha traduzida>",
                    "Avaliação": "<avaliação>"
                }}
                
                Linha da Resenha: {review}
                """
            }
        ],
        temperature=1.0
    )
    review_dct[idx] = llm_reponse.choices[0].message.content
    
for idx, review in review_dct.items():
    review = review.replace("```json", "").replace("```", "").replace("\n", "").replace("    ", "")
    review_dct[idx] = json.loads(review)

evaluation_dict = {
    'Positiva': 0,
    'Negativa': 0,
    'Neutra': 0
}

for review in review_dct.values():
    evaluation = review['Avaliação']
    evaluation_dict[evaluation] += 1

print(evaluation_dict)
print("="*100)
print("#".join(str(v) for v in review_dct.values()))