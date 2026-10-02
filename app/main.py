from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import shutil
import os
import time

from app.services.qa_service import answer_question
from app.ingestion.pdf_loader import extract_text_from_pdf
from app.ingestion.chunker import split_text
from app.ingestion.embedder import create_embeddings

from app.retrieval.vector_store import (
    create_vector_store,
    add_to_vector_store,
    save_vector_store,
    load_vector_store,
    save_chunks,
    load_chunks
)


app = FastAPI()


# -----------------------------
# CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Request Model
# -----------------------------

class QuestionRequest(BaseModel):
    question: str


# -----------------------------
# Paths
# -----------------------------

INDEX_PATH = "data/vector_store/index.faiss"
CHUNKS_PATH = "data/vector_store/chunks.pkl"


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


# -----------------------------
# Upload PDF
# -----------------------------

@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):

    start = time.time()

    os.makedirs(
        "data/documents",
        exist_ok=True
    )

    os.makedirs(
        "data/vector_store",
        exist_ok=True
    )

    # -----------------------------
    # Save PDF
    # -----------------------------

    pdf_path = (
        f"data/documents/{file.filename}"
    )

    with open(pdf_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    print(
        "FILE SAVE:",
        time.time() - start
    )

    # -----------------------------
    # Extract Text
    # -----------------------------

    text = extract_text_from_pdf(
        pdf_path
    )

    print(
        "PDF EXTRACTION:",
        time.time() - start
    )

    if not text.strip():

        return {
            "message": "PDF does not contain readable text.",
            "filename": file.filename,
            "chunks": 0
        }

    # -----------------------------
    # Create Chunks
    # -----------------------------

    chunks = split_text(text)

    print(
        "CHUNKING:",
        time.time() - start
    )

    if not chunks:

        return {
            "message": "No text chunks could be created.",
            "filename": file.filename,
            "chunks": 0
        }

    # -----------------------------
    # Add Metadata
    # -----------------------------

    document_chunks = [
        {
            "text": chunk,
            "source": file.filename
        }
        for chunk in chunks
    ]

    # -----------------------------
    # Extract Text For Embeddings
    # -----------------------------

    chunk_texts = [
        item["text"]
        for item in document_chunks
    ]

    # -----------------------------
    # Create Embeddings
    # -----------------------------

    embeddings = create_embeddings(
        chunk_texts
    )

    print(
        "EMBEDDINGS:",
        time.time() - start
    )

    # -----------------------------
    # Create / Update Vector Store
    # -----------------------------

    if os.path.exists(INDEX_PATH):

        print(
            "Existing vector store found."
        )

        index = load_vector_store(
            INDEX_PATH
        )

        index = add_to_vector_store(
            index,
            embeddings
        )

        existing_chunks = load_chunks(
            CHUNKS_PATH
        )

        all_chunks = (
            existing_chunks
            + document_chunks
        )

    else:

        print(
            "Creating new vector store."
        )

        index = create_vector_store(
            embeddings
        )

        all_chunks = document_chunks

    # -----------------------------
    # Save Vector Store
    # -----------------------------

    save_vector_store(
        index,
        INDEX_PATH
    )

    save_chunks(
        all_chunks,
        CHUNKS_PATH
    )

    print(
        "TOTAL:",
        time.time() - start
    )

    # -----------------------------
    # Response
    # -----------------------------

    return {
        "message": "PDF uploaded and processed successfully",
        "filename": file.filename,
        "chunks": len(document_chunks),
        "total_chunks": len(all_chunks)
    }


# -----------------------------
# Ask Question
# -----------------------------

@app.post("/ask")
def ask_question(
    request: QuestionRequest
):

    answer, sources = answer_question(
        request.question
    )

    return {
        "answer": answer,
        "sources": sources
    }