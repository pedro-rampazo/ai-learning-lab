from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain.globals import set_debug
from dotenv import load_dotenv
import os

set_debug(True)

load_dotenv()

model = ChatGroq(
    model='openai/gpt-oss-120b',
    temperature=0.5,
    api_key=os.getenv('GROQ_API_KEY')
)

response = model.invoke([HumanMessage(content="Qual é o melhor time do futebol brasileiro?")])
print(response.content)