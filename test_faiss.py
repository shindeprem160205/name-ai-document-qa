from app.ingestion.pdf_loader import extract_text_from_pdf
from app.ingestion.chunker import split_text
from app.ingestion.embedder import create_embeddings
from app.retrieval.vector_store import (
    create_vector_store,
    save_vector_store,
    load_vector_store,
    save_chunks,
    load_chunks
)


pdf_path = "data/documents/Unit 4_.pdf"

index_path = "data/vector_store/index.faiss"
chunks_path = "data/vector_store/chunks.pkl"


text = extract_text_from_pdf(pdf_path)

chunks = split_text(text)

embeddings = create_embeddings(chunks)

index = create_vector_store(embeddings)

save_vector_store(index, index_path)
save_chunks(chunks, chunks_path)

print("FAISS index saved.")
print("Chunks saved.")


loaded_index = load_vector_store(index_path)
loaded_chunks = load_chunks(chunks_path)

print("FAISS vectors:", loaded_index.ntotal)
print("Loaded chunks:", len(loaded_chunks))