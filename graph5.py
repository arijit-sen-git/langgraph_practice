# generate 5 random integers in loop

from langgraph.graph import StateGraph, START, END
from random import randint
from typing import List, Literal, TypedDict

class AgentState(TypedDict):
    user: str
    max_iter: int
    numbers: List[int]

def hello(state: AgentState) -> AgentState:
    print("Hi {}. Welcome to Lottery Show.".format(state["user"]))
    return state

def loop(state: AgentState) -> AgentState:
    state["max_iter"] = state["max_iter"] - 1
    state["numbers"].append(randint(1, 100))
    return state

def condition(state: AgentState) -> Literal["continue_loop", "break_loop"]:
    if state["max_iter"] <= 0:
        return "break_loop"
    else:
        return "continue_loop"

graph = StateGraph(AgentState)

graph.add_node("node_hello", hello)
graph.add_node("node_loop", loop)

graph.add_edge(START, "node_hello")
graph.add_edge("node_hello", "node_loop")

graph.add_conditional_edges(
    "node_loop",
    condition,
    {
        "continue_loop": "node_loop",
        "break_loop": END
    }
)

app = graph.compile()

input: AgentState = {"user": "Bob", "max_iter": 5, "numbers": []}
output = app.invoke(input)
print(output)
