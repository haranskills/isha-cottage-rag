from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str
    session_id: str = "default"


class SourceModel(BaseModel):
    page: int | None
    source: str | None
    chunk_index: int | None


class ChatResponse(BaseModel):
    query: str
    answer: str
    sources: list[SourceModel]
    session_id: str