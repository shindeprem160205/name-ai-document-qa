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
    save_vector_store,
    save_chunks
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):

    os.makedirs("data/documents", exist_ok=True)
    os.makedirs("data/vector_store", exist_ok=True)

    pdf_path = f"data/documents/{file.filename}"

    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(pdf_path)
    chunks = split_text(text)
    embeddings = create_embeddings(chunks)

    index = create_vector_store(embeddings)

    save_vector_store(
        index,
        "data/vector_store/index.faiss"
    )

    save_chunks(
        chunks,
        "data/vector_store/chunks.pkl"
    )

    return {
        "message": "PDF uploaded and processed successfully",
        "filename": file.filename,
        "chunks": len(chunks)
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    answer, sources = answer_question(request.question)

    return {
        "answer": answer,
        "sources": sources
    }
    
@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):

    start = time.time()

    os.makedirs("data/documents", exist_ok=True)
    os.makedirs("data/vector_store", exist_ok=True)

    pdf_path = f"data/documents/{file.filename}"

    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("FILE SAVE:", time.time() - start)

    text = extract_text_from_pdf(pdf_path)

    print("PDF EXTRACTION:", time.time() - start)

    chunks = split_text(text)

    print("CHUNKING:", time.time() - start)

    embeddings = create_embeddings(chunks)

    print("EMBEDDINGS:", time.time() - start)

    index = create_vector_store(embeddings)

    save_vector_store(
        index,
        "data/vector_store/index.faiss"
    )

    save_chunks(
        chunks,
        "data/vector_store/chunks.pkl"
    )

    print("TOTAL:", time.time() - start)

    return {
        "message": "PDF uploaded and processed successfully",
        "filename": file.filename,
        "chunks": len(chunks)
    }