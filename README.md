# 📚 AI Document Q&A — RAG Knowledge Assistant

An AI-powered document question-answering system built using **Retrieval-Augmented Generation (RAG)**.

The application allows users to upload PDF documents and ask natural-language questions about their content. Relevant document chunks are retrieved using semantic search and provided to a Gemini language model to generate grounded answers with source references.

## 🚀 Live Demo

- 🌐 **Web App:** https://name-ai-document-app.streamlit.app/
- ⚡ **FastAPI Backend:** https://name-ai-document-qa.onrender.com
- 📖 **API Documentation:** https://name-ai-document-qa.onrender.com/docs

> The backend is deployed on Render and the Streamlit frontend is deployed on Streamlit Community Cloud.

---

## 🚀 Features

- 📄 Upload PDF documents
- 📝 Extract text from PDF files
- ✂️ Split documents into smaller chunks
- 🧠 Generate embeddings using Sentence Transformers
- 🔎 Semantic similarity search using FAISS
- 📚 Support for multiple PDF documents
- 🏷️ Track source documents for retrieved content
- 🤖 Generate grounded answers using Google Gemini
- 🌐 FastAPI REST API backend
- 🎨 Streamlit web interface
- 💾 FAISS vector store
- ⚠️ Basic error handling
- 🐳 Dockerized backend
- ☁️ Cloud deployment

---

## 🏗️ System Architecture

```text
                         DOCUMENT INGESTION

    ┌──────────────┐
    │  PDF Upload  │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ Text         │
    │ Extraction   │
    │  PyMuPDF     │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │   Chunking   │
    │ LangChain    │
    │ Text Splitter│
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │  Embeddings  │
    │ MiniLM Model │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │    FAISS     │
    │ Vector Store │
    └──────┬───────┘
           │
           │
           │              QUESTION ANSWERING
           │
           │       ┌──────────────────┐
           └──────►│  User Question   │
                   └────────┬─────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │ Query Embedding  │
                   └────────┬─────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │ FAISS Similarity │
                   │     Search       │
                   └────────┬─────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │ Relevant Chunks  │
                   └────────┬─────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │ Context + Query  │
                   └────────┬─────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │   Gemini LLM     │
                   └────────┬─────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │ Answer + Sources │
                   └──────────────────┘

🧠 How RAG Works
The application uses two main pipelines.
Document Ingestion
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
FAISS Vector Store

Question Answering
User Question
 ↓
Query Embedding
 ↓
FAISS Similarity Search
 ↓
Relevant Document Chunks
 ↓
Context Construction
 ↓
Gemini
 ↓
Answer + Sources

Instead of sending the complete document to the language model, the system retrieves the most relevant chunks and provides only that context to the model.
This improves retrieval efficiency and helps keep the generated answer grounded in the uploaded documents.
🛠️ Tech Stack
Backend
- Python
- FastAPI
- Pydantic
- Uvicorn
RAG / AI
- Sentence Transformers
- all-MiniLM-L6-v2
- FAISS
- Google Gemini API
Document Processing
- PyMuPDF
- LangChain Text Splitters
Frontend
- Streamlit
Deployment
- Docker
- Render
- Streamlit Community Cloud
Development
- Git
- GitHub
- Python Virtual Environment
📁 Project Structure
ai-document-qa/
│
├── app/
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── pdf_loader.py
│   │   ├── chunker.py
│   │   └── embedder.py
│   │
│   ├── retrieval/
│   │   ├── __init__.py
│   │   └── vector_store.py
│   │
│   ├── generation/
│   │   ├── __init__.py
│   │   └── llm.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── qa_service.py
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   └── streamlit_app.py
│   │
│   ├── __init__.py
│   └── main.py
│
├── data/
│   ├── documents/
│   └── vector_store/
│
├── .dockerignore
├── .gitignore
├── .python-version
├── Dockerfile
├── README.md
└── requirements.txt

⚙️ Installation
1. Clone the repository
git clone https://github.com/shindeprem160205/name-ai-document-qa.git
cd name-ai-document-qa

2. Create a virtual environment
python -m venv .venv

3. Activate the virtual environment
Windows PowerShell:
.venv\Scripts\activate

4. Install dependencies
pip install -r requirements.txt

🔐 Environment Variables
Create a .env file in the project root:
GEMINI_API_KEY=your_gemini_api_key

The .env file is excluded from Git using .gitignore.
▶️ Running Locally
The application uses two processes: a FastAPI backend and a Streamlit frontend.
Start FastAPI Backend
python -m uvicorn app.main:app

Backend:
http://127.0.0.1:8000

Health check:
http://127.0.0.1:8000/health

Start Streamlit Frontend
Open another terminal:
streamlit run app/ui/streamlit_app.py

Application:
http://localhost:8501

🔌 API Endpoints
Health Check
GET /health

Response:
{
  "status": "healthy"
}

Upload Document
POST /upload

Uploads and processes a PDF document.
The document is:
1. Saved locally
2. Parsed into text
3. Split into chunks
4. Converted into embeddings
5. Added to the FAISS vector store
Ask Question
POST /ask

Request:
{
  "question": "What skills are mentioned in the document?"
}

Response:
{
  "answer": "The document mentions Python, SQL...",
  "sources": []
}

🔍 Retrieval Process
The application uses the following retrieval pipeline:
all-MiniLM-L6-v2
        ↓
384-dimensional embeddings
        ↓
FAISS IndexFlatL2
        ↓
Top 3 relevant chunks
        ↓
Context
        ↓
Gemini

The retrieved chunks are combined into the context provided to the language model.
📚 Multiple Document Support
The system supports adding multiple PDF documents to the same vector store.
For each uploaded document:
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
Existing FAISS Index
 ↓
Add New Vectors
 ↓
Updated Vector Store

Each chunk stores the source filename, allowing retrieved content to be traced back to the original document.
🛡️ Error Handling
The application includes basic handling for:
- Backend connection failures
- Request timeouts
- Empty PDF files
- PDFs without readable text
- Missing vector store
- Missing chunk data
- Invalid questions
- API errors
🐳 Docker
The FastAPI backend is containerized using Docker.
Build the image:
docker build -t ai-document-qa .

Run locally:
docker run --rm -p 8000:8000 --env-file .env ai-document-qa

The container exposes the FastAPI application on port 8000.
The deployed backend runs using the Docker container on Render.
☁️ Deployment
Backend
The FastAPI backend is deployed on Render using Docker.
GitHub
   ↓
Render
   ↓
Docker Build
   ↓
FastAPI

Frontend
The Streamlit frontend is deployed on Streamlit Community Cloud.
GitHub
   ↓
Streamlit Community Cloud
   ↓
Streamlit UI

The frontend communicates with the deployed FastAPI backend through the configured BACKEND_URL.
🎯 Project Objective
The objective of this project is to build a practical Retrieval-Augmented Generation system that combines document retrieval with a large language model.
The project demonstrates practical implementation of:
- Document processing
- Text chunking
- Text embeddings
- Vector search
- Semantic retrieval
- Retrieval-Augmented Generation
- Large Language Models
- REST APIs
- FastAPI
- Streamlit
- Docker
- Cloud deployment
🔮 Future Improvements
- Document deletion and management
- Chat history
- Improved source citations
- Streaming LLM responses
- User authentication
- Metadata filtering
- Retrieval reranking
- Hybrid search
- Automated testing
- External persistent storage for production-scale document/vector persistence
👨‍💻 Author
Prem Shinde
Computer Engineering Graduate
Areas of Interest
- Python Development
- AI / ML
- Data Science
- Backend Development
- RAG & LLM Applications
⭐ Project
This project was built step by step with a focus on understanding the complete RAG pipeline, from document ingestion and vector retrieval to LLM-based answer generation.
If you explore the project and have ideas for improvements, optimizations, bug fixes, or useful features, contributions and suggestions are welcome.
If you find the project useful or interesting, consider giving the repository a ⭐ Star on GitHub.
Thank you for exploring the project!
