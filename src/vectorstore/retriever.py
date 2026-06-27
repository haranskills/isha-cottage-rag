from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from src.vectorstore.faiss_store import load_vectorstore
from src.config import RETRIEVER_TOP_K
from src.logger import logger


def get_retriever():
    """
    Load FAISS vectorstore and return MMR retriever.
    MMR avoids returning duplicate/similar chunks.
    """
    vectorstore = load_vectorstore()

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": RETRIEVER_TOP_K,
            "fetch_k": RETRIEVER_TOP_K * 3  # MMR fetches more, then picks diverse ones
        }
    )

    logger.info(f"Retriever ready — top_k={RETRIEVER_TOP_K}, search=MMR")
    return retriever


def retrieve_chunks(query: str) -> list[Document]:
    """
    Retrieve top-k relevant chunks for a given query.
    """
    logger.info(f"Retrieving chunks for: '{query}'")
    retriever = get_retriever()
    chunks = retriever.invoke(query)

    logger.success(f"Retrieved {len(chunks)} chunks")
    for i, chunk in enumerate(chunks, 1):
        logger.debug(
            f"Chunk {i} | Page {chunk.metadata.get('page_number')} | "
            f"{chunk.page_content[:80]}..."
        )

    return chunks