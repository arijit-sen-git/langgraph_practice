# Simple bot with history

import os
from typing import List, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from langgraph.graph import StateGraph, START, END

load_dotenv()


class AgentState(TypedDict):
    messages: List[HumanMessage | AIMessage]


api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model = os.getenv("OPENAI_MODEL", "openai/gpt-6-luna"),
    api_key = SecretStr(api_key) if api_key else None,
    base_url = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
)


def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])

    state["messages"].append(AIMessage(content=response.content))
    print("AI: {}".format(response.content))

    return state

graph = StateGraph(AgentState)

graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()

history: List[HumanMessage | AIMessage] = []

while True:
    user_input = input("User: ")

    if user_input.strip().lower() == "exit":
        break

    history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": history})

    history = result["messages"]
