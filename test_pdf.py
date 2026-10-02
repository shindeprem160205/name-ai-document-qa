from app.ingestion.pdf_loader import extract_text_from_pdf
from app.ingestion.chunker import split_text
from app.ingestion.embedder import create_embeddings, model
from app.retrieval.vector_store import create_vector_store, search_vector_store


pdf_path = "data/documents/Unit 4_.pdf"

text = extract_text_from_pdf(pdf_path)

chunks = split_text(text)

embeddings = create_embeddings(chunks)

index = create_vector_store(embeddings)

query = "What are the global logistics trends?"

results = search_vector_store(
    index,
    query,
    model,
    chunks,
    k=3
)

print("\nRelevant chunks:\n")

for i, result in enumerate(results, 1):
    print(f"\n--- Chunk {i} ---")
    print(result)