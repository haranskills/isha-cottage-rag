from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from src.agent.state import AgentState
from src.vectorstore.retriever import retrieve_chunks
from src.config import OPENAI_API_KEY, OPENAI_MODEL
from src.logger import logger

llm = ChatOpenAI(
    model=OPENAI_MODEL,
    openai_api_key=OPENAI_API_KEY,
    temperature=0
)

GENERATOR_PROMPT = """You are a warm, knowledgeable assistant for Isha Cottage — a serene retreat stay at Isha Yoga Center, Coimbatore, run by Isha Foundation.

You have access to two knowledge sources:
1. Isha Cottage Terms and Conditions document (PDF)
2. Official Isha websites: cottage.isha.in and isha.sadhguru.org

Answer the user's question using the context below. Be helpful, specific, and friendly.

Context:
{context}

Conversation history:
{history}

User question: {query}

Guidelines:
- Give specific, complete answers — room types, pricing, timings, policies
- If the answer comes from the website, mention "According to cottage.isha.in..."
- If the answer comes from the PDF, mention the section or page
- If you find partial information, share what you have and suggest visiting cottage.isha.in or contacting support.cottage@ishafoundation.org for more
- Never say "I couldn't find that" if there is even partial relevant information in the context
- Keep the tone warm and welcoming — guests are visiting a spiritual center
"""

def retrieve_node(state: AgentState) -> AgentState:
    logger.info(f"Retrieving chunks for: {state['query']}")
    chunks = retrieve_chunks(state["query"])
    return {**state, "retrieved_chunks": chunks}


def generate_answer_node(state: AgentState) -> AgentState:
    logger.info("Generating answer...")

    chunks = state["retrieved_chunks"]
    context = "\n\n".join([
        f"[Page {c.metadata.get('page_number')}] {c.page_content}"
        for c in chunks
    ])

    history = state.get("conversation_history", [])
    history_text = "\n".join(
        [f"{m['role'].upper()}: {m['content']}" for m in history]
    ) if history else "None"

    prompt = GENERATOR_PROMPT.format(
        context=context,
        history=history_text,
        query=state["query"]
    )

    response = llm.invoke([HumanMessage(content=prompt)])
    answer = response.content.strip()

    sources = [
        {
            "page": c.metadata.get("page_number"),
            "source": c.metadata.get("source"),
            "chunk_index": c.metadata.get("chunk_index")
        }
        for c in chunks
    ]

    logger.success(f"Answer: {answer[:100]}...")
    return {**state, "answer": answer, "sources": sources}