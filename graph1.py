from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class AgentState(TypedDict):
    user: str
    message: str

def func(state: AgentState) -> AgentState:
    state["message"] = "Hi, {}. Nice to meet you.".format(state["user"])
    return state

graph = StateGraph(AgentState)
graph.add_node("node", func)

graph.add_edge(START, "node")
graph.add_edge("node", END)

app = graph.compile()

input: AgentState = {"user": "user1", "message": ""}
output = app.invoke(input)
print(output)
