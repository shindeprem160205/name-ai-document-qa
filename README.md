# 📚 AI Document Q&A

A production-style **Retrieval-Augmented Generation (RAG)** application that allows users to upload PDF documents and ask natural-language questions about their content.

The system retrieves relevant document chunks using semantic search and uses Google Gemini to generate grounded answers with source references.

## 🚀 Live Demo

**Web App:** https://name-ai-document-app.streamlit.app/

**API Docs:** https://name-ai-document-qa.onrender.com/docs

**GitHub:** https://github.com/shindeprem160205/name-ai-document-qa

---

## ✨ Features

- Upload PDF documents
- Extract and chunk document text
- Generate semantic embeddings
- FAISS similarity search
- Multiple document support
- Source-aware retrieval
- Gemini-powered answer generation
- FastAPI REST API
- Streamlit web interface
- Dockerized backend
- Cloud deployment

---

## 🏗️ Architecture

```text
PDF Upload
    ↓
Text Extraction
    ↓
Document Chunking
    ↓
Hugging Face Embeddings
    ↓
FAISS Vector Store
    ↓
User Question
    ↓
Query Embedding
    ↓
Similarity Search
    ↓
Relevant Chunks
    ↓
Context + Question
    ↓
Google Gemini
    ↓
Answer + Sources

🛠️ Tech Stack
Category	Technologies
Language	Python
Backend	FastAPI, Uvicorn, Pydantic
RAG	LangChain Text Splitters
Embeddings	Sentence Transformers, all-MiniLM-L6-v2
Vector Search	FAISS
LLM	Google Gemini
PDF Processing	PyMuPDF
Frontend	Streamlit
Deployment	Docker, Render, Streamlit Community Cloud
Version Control	Git, GitHub


📁 Project Structure
ai-document-qa/
│
├── app/
│   ├── ingestion/
│   │   ├── pdf_loader.py
│   │   ├── chunker.py
│   │   └── embedder.py
│   │
│   ├── retrieval/
│   │   └── vector_store.py
│   │
│   ├── generation/
│   │   └── llm.py
│   │
│   ├── services/
│   │   └── qa_service.py
│   │
│   ├── ui/
│   │   └── streamlit_app.py
│   │
│   └── main.py
│
├── data/
│   ├── documents/
│   └── vector_store/
│
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md

⚙️ Run Locally
1. Clone
git clone https://github.com/shindeprem160205/name-ai-document-qa.git
cd name-ai-document-qa

2. Create virtual environment
python -m venv .venv

3. Activate
Windows PowerShell:
.venv\Scripts\activate

4. Install dependencies
pip install -r requirements.txt

5. Configure environment
Create .env:
GEMINI_API_KEY=your_gemini_api_key

6. Start FastAPI
python -m uvicorn app.main:app

API:
http://127.0.0.1:8000

Swagger:
http://127.0.0.1:8000/docs

7. Start Streamlit
In another terminal:
streamlit run app/ui/streamlit_app.py

Frontend:
http://localhost:8501

🔌 API
Health Check
GET /health

{
  "status": "healthy"
}

Upload PDF
POST /upload

Processes the uploaded PDF and adds its chunks to the FAISS vector store.
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

🐳 Docker
Build:
docker build -t ai-document-qa .

Run:
docker run --rm -p 8000:8000 --env-file .env ai-document-qa

☁️ Deployment
Backend
Deployed on Render using Docker.
GitHub → Render → Docker → FastAPI

Frontend
Deployed on Streamlit Community Cloud.
GitHub → Streamlit Cloud → Streamlit

The Streamlit frontend communicates with the deployed FastAPI backend through BACKEND_URL.
🔮 Future Improvements
- Chat history
- Document management and deletion
- Improved source citations
- Streaming responses
- User authentication
- Metadata filtering
- Retrieval reranking
- Hybrid search
- Automated testing
- External persistent storage
👨‍💻 Author
Prem Shinde
Computer Engineering Graduate
Interests: Python • AI/ML • Data Science • Backend Development • RAG & LLM Applications
