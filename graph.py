from joke import fetch_joke
from joke import show_menu
from joke import update_category
from joke import exit_bot
from joke import route_choice
from joke import JokeState
from langgraph.graph import StateGraph, END, START
from langgraph.graph.state import CompiledStateGraph



def build_joke_graph() -> CompiledStateGraph:
    workflow = StateGraph(JokeState)

    workflow.add_node("show_menu", show_menu)
    workflow.add_node("fetch_joke", fetch_joke)
    workflow.add_node("update_category", update_category)
    workflow.add_node("exit_bot", exit_bot)

    workflow.set_entry_point("show_menu")

    workflow.add_conditional_edges(
        "show_menu", 
        route_choice,
        {
            "fetch_joke": "fetch_joke",
            "update_category": "update_category",
            "exit_bot" : "exit_bot",
        }
    )

    workflow.add_edge("fetch_joke", "show_menu")
    workflow.add_edge("update_category", "fetch_joke")
    workflow.add_edge("exit_bot", END)

    return workflow.compile()



 


