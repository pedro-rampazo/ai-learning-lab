from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_core.globals import set_debug
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from pydantic import Field, BaseModel
from dotenv import load_dotenv
import os

# set_debug(True)

load_dotenv()

model = ChatGroq(
    model='openai/gpt-oss-120b',
    temperature=0.5,
    api_key=os.getenv('GROQ_API_KEY')
)
# ========== SCHEMAS ==========
class FootballTeam(BaseModel):
    team:str = Field("O maior time de futebol.")
    reason:str = Field("Motivo pelo qual o time é o maior.")
    
class Player(BaseModel):
    team:str = Field("O maior time de futebol.")
    player:str = Field("O maior jogador do time de futebol.")
    
class Supporter(BaseModel):
    team:str = Field("O maior time de futebol.")
    supporters_quantity:int = Field("Quantidade de torcedores da equipe.")

# ========== PARSERS ==========
football_team_parser = JsonOutputParser(pydantic_object=FootballTeam)
player_parser = JsonOutputParser(pydantic_object=Player)
supporter_parser = JsonOutputParser(pydantic_object=Supporter)

# ========== PROMPTS ==========
nacionality_prompt = PromptTemplate(
    template="""
        Pontue o maior time {nacionality} de futebol.
        {output}
    """,
    input_variables=["nacionality"],
    partial_variables={"output": football_team_parser.get_format_instructions()}
)
player_prompt = PromptTemplate(
    template="""
        Sugira o maior jogador da história do time {team}.
        {output}
    """,
    input_variables=["team"],
    partial_variables={"output": player_parser.get_format_instructions()}
)
supporter_prompt = PromptTemplate(
    template="""
        Qual é o número de torcedores do time {team}.
        {output}
    """,
    input_variables=['team'],
    partial_variables={"output": supporter_parser.get_format_instructions()}
)

jail_one = nacionality_prompt | model | football_team_parser
jail_two = player_prompt | model | player_parser
jail_three = supporter_prompt | model | supporter_parser

jail = jail_one | jail_two | jail_three

response = jail.invoke(
    {
        "nacionality": "brasileiro"
    }
)
print(response)