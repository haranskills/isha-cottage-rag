from src.logger import logger

# In-memory store — { session_id: [messages] }
session_store: dict[str, list] = {}


def get_history(session_id: str) -> list:
    return session_store.get(session_id, [])


def update_history(session_id: str, query: str, answer: str) -> None:
    if session_id not in session_store:
        session_store[session_id] = []

    session_store[session_id].append({"role": "user", "content": query})
    session_store[session_id].append({"role": "assistant", "content": answer})

    # Keep last 10 exchanges only
    session_store[session_id] = session_store[session_id][-20:]
    logger.debug(f"Session {session_id} history updated — {len(session_store[session_id])} messages")


def clear_history(session_id: str) -> None:
    if session_id in session_store:
        del session_store[session_id]
        logger.info(f"Session {session_id} cleared")