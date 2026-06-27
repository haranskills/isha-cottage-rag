from src.vectorstore.retriever import retrieve_chunks

def test_retriever():
    # Use a question relevant to your T&C document
    query = "What are the cancellation terms for Isha Cottage?"
    chunks = retrieve_chunks(query)

    assert len(chunks) > 0, "No chunks retrieved!"

    print("\n--- Retrieved Chunks ---")
    for i, chunk in enumerate(chunks, 1):
        print(f"\nChunk {i} | Page {chunk.metadata.get('page_number')}")
        print(chunk.page_content[:200])
        print("-" * 40)

if __name__ == "__main__":
    test_retriever()