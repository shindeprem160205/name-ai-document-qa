import os
import time

from app.retrieval.vector_store import (
    load_vector_store,
    load_chunks,
    search_vector_store
)
from app.ingestion.embedder import model
from app.generation.llm import generate_answer

INDEX_PATH = "data/vector_store/index.faiss"
CHUNKS_PATH = "data/vector_store/chunks.pkl"


def answer_question(question):

    start = time.time()

    print("\n========== ASK START ==========")

    print("1. Loading FAISS...")
    index = load_vector_store(INDEX_PATH)
    print("   FAISS loaded:", time.time() - start)

    print("2. Loading chunks...")
    chunks = load_chunks(CHUNKS_PATH)
    print("   Chunks loaded:", time.time() - start)

    print("3. Searching vector store...")
    relevant_chunks = search_vector_store(
        index,
        question,
        model,
        chunks,
        k=3
    )
    print("   Search done:", time.time() - start)

    context = "\n\n".join(relevant_chunks)

    print("4. Calling Gemini...")
    answer = generate_answer(question, context)
    print("   Gemini done:", time.time() - start)

    print("========== ASK END ==========\n")

    return answer, relevant_chunks