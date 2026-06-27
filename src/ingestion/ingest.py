from src.ingestion.loader import load_pdf
from src.ingestion.chunker import chunk_pages
from src.ingestion.web_scraper import scrape_websites
from src.vectorstore.faiss_store import save_vectorstore
from src.logger import logger

PDF_PATH = "./data/isha_cottage_tc.pdf"


def run_ingestion():
    logger.info("Starting ingestion pipeline...")

    # Step 1 — Load PDF
    pages = load_pdf(PDF_PATH)
    pdf_chunks = chunk_pages(pages)
    logger.info(f"PDF chunks: {len(pdf_chunks)}")

    # Step 2 — Scrape websites
    web_docs = scrape_websites()
    from src.ingestion.chunker import chunk_web_docs
    web_chunks = chunk_web_docs(web_docs)
    logger.info(f"Web chunks: {len(web_chunks)}")

    # Step 3 — Combine and save
    all_chunks = pdf_chunks + web_chunks
    logger.info(f"Total chunks: {len(all_chunks)}")
    save_vectorstore(all_chunks)

    logger.success("Ingestion pipeline complete.")


if __name__ == "__main__":
    run_ingestion()