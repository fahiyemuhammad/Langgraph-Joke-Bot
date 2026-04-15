import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel
from typing import Annotated, List , Literal
from operator import add
from pyjokes import get_joke


load_dotenv()

key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(api_key=key, temperature=0.5, model="llama-3.1-8b-instant")

class Joke(BaseModel):
    text: str
    category: str

class JokeState(BaseModel):
    jokes: Annotated[List[Joke], add] = []
    jokes_choice: Literal["n", "c", "q"] = "n"
    category:str = "neutral"
    language : str = "en"
    quit: bool = False


def show_menu(state:JokeState) -> dict:
    user_input = input("[n] Next  [c] Category  [q] Quit\n> ").strip().lower()
    return {"jokes_choice": user_input}  

def fetch_joke(state: JokeState) -> dict:
    joke_text = get_joke(language=state.language, category=state.category)
    new_joke = Joke(text=joke_text, category=state.category)
    print("-------------------------------------------------------------")
    print("")
    print(f"😂    {new_joke.text}    😂")
    print("-------------------------------------------------------------")

    return {"jokes": [new_joke]}

def update_category(state: JokeState):
    categories = ["neutral", "chuck", "all"]
    selection = int(input("Select category [0=neutral, 1=chuck, 2=all]: ").strip())
    return {"category": categories[selection]}

def exit_bot(state: JokeState) -> dict:
    return {"quit": True}

def route_choice(state: JokeState)  -> str:
    if state.jokes_choice == 'n':
        return "fetch_joke"
    elif state.jokes_choice == 'c':
        return "update_category"
    elif state.jokes_choice == 'q':
        return "exit_bot"
    return "exit_bot"