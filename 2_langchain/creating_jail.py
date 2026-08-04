from openai import OpenAI
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.globals import set_debug
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_openai import ChatOpenAI
from pydantic import Field ,BaseModel


set_debug(True)

load_dotenv()

class Destino(BaseModel):
    cidade:str = Field(description="A cidade recomentada para visitar")
    motivo:str = Field(description="Motivo pelo qual é interessante visitar essa cidade")
    
class Restaurante(BaseModel):
    cidade:str = Field("A cidade recomedada para visitar")
    restaurante:str = Field("Restaurantes recomendados na cidade")
    
parseador_destino = JsonOutputParser(pydantic_object=Destino)
parseador_restaurante = JsonOutputParser(pydantic_object=Restaurante)

prompt_destino = PromptTemplate(
    template="""
        Sugira uma cidade dado o meu interesse por {interesse}.
        {formato_de_saida}
    """,
    input_variables=["interesse"],
    partial_variables={"formato_de_saida": parseador_destino.get_format_instructions()}
)

prompt_restaurante = PromptTemplate(
    template="""
        Sugira restaurantes populares entre locais em {cidade}.
        {formato_de_saida}
    """,
    partial_variables={"formato_de_saida": parseador_restaurante.get_format_instructions()}
)

prompt_cultural = PromptTemplate(
    template="Sugira atividades e locais culturais em {cidade}"
)

modelo = ChatOpenAI(
    base_url=os.getenv("LLM_PORT"),
    temperature=0.5,
    api_key="lm-studio"
)

cadeia_1 = prompt_destino | modelo | parseador_destino
# cadeia_2 = prompt_restaurante | modelo | parseador_restaurante
# cadeia_3 = prompt_cultural | modelo | StrOutputParser()


# cadeia = (cadeia_1 | cadeia_2 | cadeia_3)

resposta = cadeia_1.invoke(
    {
        "interesse": "praias"
    }
)

# print(resposta)
