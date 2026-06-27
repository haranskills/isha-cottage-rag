import requests
from bs4 import BeautifulSoup
from langchain.schema import Document
from src.logger import logger

URLS = [
    "https://cottage.isha.in",
    "https://cottage.isha.in/terms-conditions/",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def scrape_url(url: str) -> Document | None:
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            logger.warning(f"Could not reach {url} — status {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        clean_text = " ".join(lines)

        if len(clean_text) < 100:
            logger.warning(f"Too little content from {url}, skipping.")
            return None

        logger.success(f"Scraped {url} — {len(clean_text)} chars")

        return Document(
            page_content=clean_text,
            metadata={
                "source": url,
                "page_number": 0,
                "chunk_index": 0
            }
        )

    except Exception as e:
        logger.warning(f"Failed to scrape {url}: {e}")
        return None


def scrape_websites() -> list[Document]:
    logger.info("Scraping Isha websites...")
    docs = []
    for url in URLS:
        doc = scrape_url(url)
        if doc:
            docs.append(doc)
    logger.success(f"Scraped {len(docs)} pages successfully")
    return docs