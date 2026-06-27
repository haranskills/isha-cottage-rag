from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.api.models import ChatRequest, ChatResponse, SourceModel
from src.api.memory import get_history, update_history, clear_history
from src.agent.graph import rag_agent
from src.logger import logger

app = FastAPI(
    title="Isha Cottage RAG Agent",
    description="AI-powered Terms & Conditions assistant for Isha Cottage",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def root():
    return {"status": "running", "agent": "Isha Cottage RAG Agent v1.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    logger.info(f"[{request.session_id}] Query: {request.query}")

    try:
        history = get_history(request.session_id)

        initial_state = {
            "query": request.query,
            "retrieved_chunks": [],
            "answer": "",
            "sources": [],
            "conversation_history": history
        }

        result = rag_agent.invoke(
            initial_state,
            config={"recursion_limit": 10}
        )

        update_history(
            request.session_id,
            request.query,
            result["answer"]
        )

        sources = [SourceModel(**s) for s in result["sources"]]

        return ChatResponse(
            query=result["query"],
            answer=result["answer"],
            sources=sources,
            session_id=request.session_id
        )

    except Exception as e:
        logger.error(f"Agent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/session/{session_id}")
def clear_session(session_id: str):
    clear_history(session_id)
    return {"message": f"Session {session_id} cleared"}