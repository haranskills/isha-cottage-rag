from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from src.config import CHUNK_SIZE, CHUNK_OVERLAP
from src.logger import logger


def chunk_pages(pages: list[dict]) -> list[Document]:
    """
    Split pages into chunks and return LangChain Document objects.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    all_chunks = []

    for page in pages:
        chunks = splitter.split_text(page["text"])

        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk,
                metadata={
                    "source": page["source"],
                    "page_number": page["page_number"],
                    "chunk_index": i
                }
            )
            all_chunks.append(doc)

    logger.success(f"Created {len(all_chunks)} chunks from {len(pages)} pages")
    return all_chunks

def chunk_web_docs(docs: list[Document]) -> list[Document]:
    """
    Chunk web scraped documents.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    all_chunks = []

    for doc in docs:
        chunks = splitter.split_text(doc.page_content)
        for i, chunk in enumerate(chunks):
            all_chunks.append(Document(
                page_content=chunk,
                metadata={
                    "source": doc.metadata["source"],
                    "page_number": 0,
                    "chunk_index": i
                }
            ))

    logger.success(f"Created {len(all_chunks)} chunks from {len(docs)} web pages")
    return all_chunks