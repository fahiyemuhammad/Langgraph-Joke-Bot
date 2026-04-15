from graph import build_joke_graph
from joke import JokeState

def main():
    graph = build_joke_graph()

    initial_state = JokeState()

    graph.invoke(initial_state)


if __name__ == "__main__":
    main()