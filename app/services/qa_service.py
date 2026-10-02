import os

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

    # -----------------------------
    # Check Vector Store
    # -----------------------------

    if not os.path.exists(INDEX_PATH):

        raise FileNotFoundError(
            "Vector store not found. Upload a document first."
        )

    if not os.path.exists(CHUNKS_PATH):

        raise FileNotFoundError(
            "Chunks file not found. Upload a document first."
        )

    # -----------------------------
    # Load Vector Store
    # -----------------------------

    index = load_vector_store(
        INDEX_PATH
    )

    # -----------------------------
    # Load Chunks
    # -----------------------------

    chunks = load_chunks(
        CHUNKS_PATH
    )

    # -----------------------------
    # Search Relevant Chunks
    # -----------------------------

    relevant_chunks = search_vector_store(
        index,
        question,
        model,
        chunks,
        k=3
    )

    # -----------------------------
    # Build Context
    # -----------------------------

    context = "\n\n".join(
        chunk["text"]
        for chunk in relevant_chunks
    )

    # -----------------------------
    # Generate Answer
    # -----------------------------

    answer = generate_answer(
        question,
        context
    )

    return answer, relevant_chunks