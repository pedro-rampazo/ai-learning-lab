from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client_openai = OpenAI(
    base_url=os.getenv("LLM_PORT"),
    api_key="lm-studio"
)

llm_reponse = client_openai.chat.completions.create(
    model="google/gemma-3-1b",
    messages=[
        {"role": "system", "content": "Você é um assistente de IA que sempre responde de forma muito sarcástica"},
        {"role": "user", "content": "O que é IA Generativa?"}
    ],
    temperature=1.0
)

print(llm_reponse.choices[0].message.content)