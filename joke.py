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
    jokes_choice: Literal["n", "c", "l" ,"q"] = "n"
    category:str = "neutral"
    language : str = "en"
    quit: bool = False


def show_menu(state:JokeState) -> dict:
    while True:
        user_input = input("[n] Next  [c] Category [l] Language [q] Quit\n> ").strip().lower()
        if user_input in ["n", "c", "q", "l"]:
            return {"jokes_choice": user_input}  
        print("❌  Wrong input! Please enter n, c, l, or q.   ❌")

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

def update_language(state: JokeState):
    languages = ["en", "de", "es"]
    selection = int(input("Select language [0=en, 1=de, 2=es]: ").strip())
    return {"language": languages[selection]}

def exit_bot(state: JokeState) -> dict:
    return {"quit": True}

def route_choice(state: JokeState)  -> str:
    if state.jokes_choice == 'n':
        return "fetch_joke"
    elif state.jokes_choice == 'c':
        return "update_category"
    elif state.jokes_choice == "l":
        return "update_language"
    elif state.jokes_choice == 'q':
        return "exit_bot"
    return "exit_bot"