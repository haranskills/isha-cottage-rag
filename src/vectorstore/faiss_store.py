from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from pathlib import Path
from src.config import OPENAI_API_KEY, EMBEDDING_MODEL, FAISS_DB_PATH, FAISS_INDEX_NAME
from src.logger import logger


def get_embeddings():
    return OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY
    )


def save_vectorstore(chunks: list[Document]) -> None:
    """
    Embed chunks and save FAISS index to disk.
    """
    logger.info(f"Embedding {len(chunks)} chunks — this may take a moment...")

    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    Path(FAISS_DB_PATH).mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(f"{FAISS_DB_PATH}/{FAISS_INDEX_NAME}")

    logger.success(f"FAISS index saved to {FAISS_DB_PATH}/{FAISS_INDEX_NAME}")


def load_vectorstore() -> FAISS:
    """
    Load existing FAISS index from disk.
    """
    index_path = f"{FAISS_DB_PATH}/{FAISS_INDEX_NAME}"

    if not Path(index_path).exists():
        raise FileNotFoundError(
            f"No FAISS index found at {index_path}. Run ingestion first."
        )

    embeddings = get_embeddings()
    vectorstore = FAISS.load_local(
        index_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    logger.success(f"FAISS index loaded from {index_path}")
    return vectorstore