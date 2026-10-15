# conditional edge

from langgraph.graph import StateGraph, START, END
from typing import Literal, TypedDict

class AgentState(TypedDict):
    num1: int
    num2: int
    op: str
    result: int | None

def add(state: AgentState) -> AgentState:
    state["result"] = state["num1"] + state["num2"]
    return state

def sub(state: AgentState) -> AgentState:
    state["result"] = state["num1"] - state["num2"]
    return state

def decide(state: AgentState) -> Literal["op_add", "op_sub"]:
    if state["op"] == "+":
        return "op_add"
    if state["op"] == "-":
        return "op_sub"
    else:
        raise ValueError("Invalid Operator")

graph = StateGraph(AgentState)

graph.add_node("node_add", add)
graph.add_node("node_sub", sub)

graph.add_conditional_edges(
    START,
    decide,
    {
        "op_add": "node_add",
        "op_sub": "node_sub"
    }
)

graph.add_edge("node_add", END)
graph.add_edge("node_sub", END)

app = graph.compile()

try:
    input: AgentState = {"num1": 5, "num2": 10, "op": "+", "result": None}
    output = app.invoke(input)
    print(output)
except ValueError as e:
    print(e)
