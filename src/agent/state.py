from typing import TypedDict


class AgentState(TypedDict):
    query: str
    retrieved_chunks: list
    answer: str
    sources: list
    conversation_history: list