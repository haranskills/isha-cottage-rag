from src.agent.graph import rag_agent
from src.logger import logger


def test_agent():
    # Use a real question from your T&C PDF
    initial_state = {
        "query": "What are the check-in and check-out timings at Isha Cottage?",
        "rewritten_query": "",
        "retrieved_chunks": [],
        "relevant_chunks": [],
        "answer": "",
        "sources": [],
        "hallucination_score": "",
        "retry_count": 0,
        "conversation_history": []
    }

    logger.info("Running RAG agent test...")
    
    result = rag_agent.invoke(
        initial_state,
        config={"recursion_limit": 10}
    )

    print("\n" + "="*50)
    print("QUERY:", result["query"])
    print("REWRITTEN:", result["rewritten_query"])
    print("\nANSWER:")
    print(result["answer"])
    print("\nSOURCES:")
    for s in result["sources"]:
        print(f"  - Page {s['page']} | {s['source']}")
    print("="*50)


if __name__ == "__main__":
    test_agent()