from langgraph.graph import StateGraph, START, END
from typing import List, TypedDict
import numpy

class AgentState(TypedDict):
    values: List[int]
    result: int | None
    op: str

def func(state: AgentState) -> AgentState:
    if state["op"] == "+":
        state["result"] = int(numpy.sum(state["values"]))
    elif state["op"] == "*":
        state["result"] = int(numpy.prod(state["values"]))
    else:
        raise ValueError("Unsupported Operation")

    return state

graph = StateGraph(AgentState)
graph.add_node("node1", func)

graph.add_edge(START, "node1")
graph.add_edge("node1", END)

app = graph.compile()

try:
    input: AgentState = {"values": [1, 2, 3, 4], "op": "*", "result": None}
    output = app.invoke(input)
    print(output)
except ValueError as e:
    print(e)
