import fitz  # PyMuPDF
from pathlib import Path
from src.logger import logger


def load_pdf(pdf_path: str) -> list[dict]:
    """
    Load PDF and return list of pages with text and metadata.
    """
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found at: {pdf_path}")

    logger.info(f"Loading PDF: {path.name}")
    pages = []

    doc = fitz.open(pdf_path)
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        text = clean_text(text)

        if not text.strip():
            logger.warning(f"Page {page_num} is empty, skipping.")
            continue

        pages.append({
            "page_number": page_num,
            "text": text,
            "source": path.name
        })

    doc.close()
    logger.success(f"Loaded {len(pages)} pages from {path.name}")
    return pages


def clean_text(text: str) -> str:
    """
    Basic text cleaning — remove excess whitespace.
    """
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]  # remove blank lines
    return " ".join(lines)