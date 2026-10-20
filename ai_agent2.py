# simple bot with streaming output, no history

import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from langgraph.graph import StateGraph, START, END

load_dotenv()


class AgentState(TypedDict):
    messages: HumanMessage

api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model = os.getenv("OPENAI_MODEL", "openai/gpt-6-luna"),
    api_key = SecretStr(api_key) if api_key else None,
    base_url = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
)


def process(state: AgentState) -> AgentState:
    for chunk in llm.stream(state["messages"].content):
        if isinstance(chunk.content, str):
            print(chunk.content, end = "", flush = True)

    print()
    return state


graph = StateGraph(AgentState)

graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()


while True:
    user_input = input("User: ")

    if user_input.strip().lower() == "exit":
        break

    agent.invoke({"messages": HumanMessage(content = user_input)})
