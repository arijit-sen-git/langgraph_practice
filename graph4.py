from langgraph.graph import StateGraph, START, END
from typing import Literal, TypedDict

class AgentState(TypedDict):
    num1: int
    num2: int
    num3: int
    num4: int
    op1: str
    op2: str
    result1: int | None
    result2: int | None

def add1(state: AgentState) -> AgentState:
    state["result1"] = state["num1"] + state["num2"]
    return state

def sub1(state: AgentState) -> AgentState:
    state["result1"] = state["num1"] - state["num2"]
    return state

def decide1(state: AgentState) -> Literal["op1_add", "op1_sub"]:
    if state["op1"] == "+":
        return "op1_add"
    if state["op1"] == "-":
        return "op1_sub"
    else:
        raise ValueError("Invalid Operator 1")

def add2(state: AgentState) -> AgentState:
    state["result2"] = state["num3"] + state["num4"]
    return state

def sub2(state: AgentState) -> AgentState:
    state["result2"] = state["num3"] - state["num4"]
    return state

def decide2(state: AgentState) -> Literal["op2_add", "op2_sub"]:
    if state["op2"] == "+":
        return "op2_add"
    if state["op2"] == "-":
        return "op2_sub"
    else:
        raise ValueError("Invalid Operator 2")

def dummy(state: AgentState) -> AgentState:
    return state

graph = StateGraph(AgentState)

graph.add_node("node1_add", add1)
graph.add_node("node1_sub", sub1)
graph.add_node("node_dummy", dummy)
graph.add_node("node2_add", add2)
graph.add_node("node2_sub", sub2)

graph.add_conditional_edges(
    START,
    decide1,
    {
        "op1_add": "node1_add",
        "op1_sub": "node1_sub"
    }
)

graph.add_edge("node1_add", "node_dummy")
graph.add_edge("node1_sub", "node_dummy")

graph.add_conditional_edges(
    "node_dummy",
    decide2,
    {
        "op2_add": "node2_add",
        "op2_sub": "node2_sub"
    }
)

graph.add_edge("node2_add", END)
graph.add_edge("node2_sub", END)

app = graph.compile()

try:
    input: AgentState = {"num1": 1, "num2": 2, "num3": 9, "num4": 6, "op1": "+", "op2": "-", "result1": None, "result2": None}
    output = app.invoke(input)
    print(output)
except ValueError as e:
    print(e)