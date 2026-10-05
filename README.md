# 📚 AI Document Q&A

> A production-style **Retrieval-Augmented Generation (RAG)** application for querying PDF documents using semantic search and Google Gemini.

The application allows users to upload PDF documents and ask natural-language questions about their content. Relevant document chunks are retrieved using semantic search and provided to Gemini to generate grounded answers with source references.

---

## 🚀 Live Demo

| Resource | Link |
|---|---|
| 🌐 **Web Application** | [Open AI Document Q&A](https://name-ai-document-app.streamlit.app/) |
| 📖 **API Documentation** | [Open Swagger UI](https://name-ai-document-qa.onrender.com/docs) |
| 💻 **GitHub Repository** | [View Source Code](https://github.com/shindeprem160205/name-ai-document-qa) |

---

## ✨ Features

- 📄 Upload PDF documents
- 📝 Extract text from PDF files
- ✂️ Split documents into meaningful chunks
- 🧠 Generate semantic embeddings
- 🔎 Perform similarity search using FAISS
- 📚 Support multiple PDF documents
- 🏷️ Track source documents for retrieved chunks
- 🤖 Generate grounded answers using Google Gemini
- 🌐 FastAPI REST API
- 🎨 Streamlit web interface
- 🐳 Dockerized backend
- ☁️ Cloud deployment

---

## 🏗️ System Architecture

```mermaid
flowchart TD

    A[📄 PDF Upload] --> B[📝 Text Extraction]
    B --> C[✂️ Document Chunking]
    C --> D[🧠 Hugging Face Embeddings]
    D --> E[(🔎 FAISS Vector Store)]

    F[❓ User Question] --> G[🧠 Query Embedding]
    G --> E

    E --> H[📚 Relevant Chunks]
    H --> I[📋 Context + Question]
    I --> J[🤖 Google Gemini]
    J --> K[💬 Answer + Sources]

RAG Pipeline
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
Relevant Chunks
 ↓
Context Construction
 ↓
Google Gemini
 ↓
Answer + Sources

🧠 How It Works
The system is divided into two major pipelines.
1. Document Ingestion
When a PDF is uploaded:
PDF
 ↓
PyMuPDF
 ↓
Extracted Text
 ↓
LangChain Text Splitter
 ↓
Document Chunks
 ↓
Sentence Transformer
 ↓
Embeddings
 ↓
FAISS

2. Question Answering
When a user asks a question:
Question
 ↓
Query Embedding
 ↓
FAISS Similarity Search
 ↓
Top Relevant Chunks
 ↓
Context
 ↓
Gemini
 ↓
Grounded Answer
 ↓
Source References

The complete document is not sent to the LLM. Instead, the system retrieves the most relevant chunks and uses them as context for answer generation.
🛠️ Tech Stack
Category	Technologies
🐍 Language	Python
⚡ Backend	FastAPI, Uvicorn, Pydantic
🔗 RAG	LangChain Text Splitters
🧠 Embeddings	Sentence Transformers
📐 Embedding Model	all-MiniLM-L6-v2
🔎 Vector Search	FAISS
🤖 LLM	Google Gemini
📄 PDF Processing	PyMuPDF
🎨 Frontend	Streamlit
🐳 Containerization	Docker
☁️ Backend Deployment	Render
☁️ Frontend Deployment	Streamlit Community Cloud
🔧 Version Control	Git, GitHub


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
1️⃣ Clone the Repository
git clone https://github.com/shindeprem160205/name-ai-document-qa.git
cd name-ai-document-qa

2️⃣ Create Virtual Environment
python -m venv .venv

3️⃣ Activate Environment
Windows PowerShell
.venv\Scripts\activate

4️⃣ Install Dependencies
pip install -r requirements.txt

5️⃣ Configure Environment Variables
Create a .env file:
GEMINI_API_KEY=your_gemini_api_key

⚠️ Never commit your .env file or API keys to GitHub.

6️⃣ Start FastAPI Backend
python -m uvicorn app.main:app

Backend:
http://127.0.0.1:8000

Swagger:
http://127.0.0.1:8000/docs

7️⃣ Start Streamlit Frontend
Open another terminal:
streamlit run app/ui/streamlit_app.py

Frontend:
http://localhost:8501

🔌 API Endpoints
❤️ Health Check
GET /health

Response:
{
  "status": "healthy"
}

📄 Upload PDF
POST /upload

Processes the uploaded PDF and adds its chunks to the FAISS vector store.
Processing flow:
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
FAISS

💬 Ask Question
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

🔎 Retrieval Architecture
The retrieval system uses:
all-MiniLM-L6-v2
        ↓
384-dimensional Embeddings
        ↓
FAISS IndexFlatL2
        ↓
Similarity Search
        ↓
Top 3 Relevant Chunks
        ↓
Context
        ↓
Gemini

Each retrieved chunk also stores its source filename, allowing the application to show where the information came from.
📚 Multiple Document Support
The application supports adding multiple PDF documents to the same vector store.
PDF 1 ──┐
PDF 2 ──┤
PDF 3 ──┤
         ↓
    Text Extraction
         ↓
      Chunking
         ↓
     Embeddings
         ↓
 Existing FAISS Index
         ↓
   Updated Vector Store

Each chunk retains its source document information.
🛡️ Error Handling
The application includes handling for common failures such as:
- Backend connection errors
- Request timeouts
- Invalid questions
- Empty documents
- PDFs without readable text
- Missing vector store
- Missing chunk data
- API errors
🐳 Docker
Build Image
docker build -t ai-document-qa .

Run Container
docker run --rm -p 8000:8000 --env-file .env ai-document-qa

The Dockerized FastAPI backend is deployed on Render.
☁️ Deployment
Backend
GitHub
   ↓
Render
   ↓
Docker Build
   ↓
FastAPI

Frontend
GitHub
   ↓
Streamlit Community Cloud
   ↓
Streamlit UI

The Streamlit frontend communicates with the deployed FastAPI backend through BACKEND_URL.
🔮 Future Improvements
- 💬 Chat history
- 📂 Document management and deletion
- 📌 Improved source citations
- ⚡ Streaming LLM responses
- 🔐 User authentication
- 🏷️ Metadata filtering
- 🎯 Retrieval reranking
- 🔀 Hybrid search
- 🧪 Automated testing
- 💾 External persistent storage
👨‍💻 Author
Prem Shinde
Computer Engineering Graduate
Interests
Python · AI/ML · Data Science · Backend Development · RAG · LLM Applications
