from langgraph.graph import StateGraph, END
from src.agent.state import AgentState
from src.agent.nodes import retrieve_node, generate_answer_node
from src.logger import logger


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("generate_answer", generate_answer_node)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate_answer")
    graph.add_edge("generate_answer", END)

    return graph.compile()


rag_agent = build_graph()