# guessing a random integer in loop and 3 edges in conditional edge

from langgraph.graph import StateGraph, START, END
from random import randint
from typing import Literal, TypedDict

class AgentState(TypedDict):
    user: str
    req_int: int
    max_iter: int

def hello(state: AgentState) -> AgentState:
    print("Hi {}. Welcome to Lottery Show.".format(state["user"]))
    return state

def loop(state: AgentState) -> AgentState:
    state["max_iter"] = state["max_iter"] - 1
    return state

def condition(state: AgentState) -> Literal["continue_loop", "break_loop_found", "break_loop_not_found"]:
    rand_int = randint(1, 10)

    if rand_int == state["req_int"]:
        return "break_loop_found"

    elif state["max_iter"] <= 0:
        return "break_loop_not_found"

    else:
        return "continue_loop"

def end_found(state: AgentState) -> AgentState:
    print("Congratulations! Required integer {} was found.".format(state["req_int"]))
    return state

def end_not_found(state: AgentState) -> AgentState:
    print("Required integer {} was not found.".format(state["req_int"]))
    return state

graph = StateGraph(AgentState)

graph.add_node("node_hello", hello)
graph.add_node("node_loop", loop)
graph.add_node("node_end_found", end_found)
graph.add_node("node_end_not_found", end_not_found)

graph.add_edge(START, "node_hello")
graph.add_edge("node_hello", "node_loop")

graph.add_conditional_edges(
    "node_loop",
    condition,
    {
        "continue_loop": "node_loop",
        "break_loop_found": "node_end_found",
        "break_loop_not_found": "node_end_not_found"
    }
)

graph.add_edge("node_end_found", END)
graph.add_edge("node_end_not_found", END)

app = graph.compile()

input: AgentState = {"user": "Bob", "max_iter": 5, "req_int": 7}
output = app.invoke(input)
print(output)
