
```markdown
# 📚 AI Document Q&A — RAG Knowledge Assistant

An AI-powered Document Question Answering system built using **Retrieval-Augmented Generation (RAG)**.

The application allows users to upload PDF documents and ask questions about their content. The system retrieves relevant document chunks using semantic search and uses a Gemini language model to generate grounded answers.

---

## 🚀 Features

- 📄 Upload PDF documents
- 📝 Extract text from PDF files
- ✂️ Split documents into smaller chunks
- 🧠 Generate text embeddings using Sentence Transformers
- 🔎 Semantic similarity search using FAISS
- 📚 Support for multiple PDF documents
- 🏷️ Track the source document for retrieved chunks
- 🤖 Generate answers using Google Gemini
- 🌐 FastAPI backend
- 🎨 Streamlit user interface
- 💾 Persistent FAISS vector store
- ⚠️ Basic error handling for invalid/empty documents

---

## 🏗️ Architecture

```text
                ┌─────────────────┐
                │   PDF Upload    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Text Extraction│
                │    PyMuPDF      │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │    Chunking     │
                │ LangChain Split │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Embeddings    │
                │ MiniLM Model    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │      FAISS      │
                │  Vector Store   │
                └────────┬────────┘
                         │
                         │
User Question ───────────┘
        │
        ▼
┌─────────────────┐
│ Query Embedding │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Similarity Search│
│   Top-K Chunks  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Context + Query │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Gemini LLM     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Answer + Sources│
└─────────────────┘
```

---

## 🧠 How RAG Works

The application follows two main pipelines.

### Document Ingestion

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
FAISS Vector Store
```

### Question Answering

```text
User Question
 ↓
Question Embedding
 ↓
FAISS Similarity Search
 ↓
Relevant Document Chunks
 ↓
Context Construction
 ↓
Gemini
 ↓
Answer
```

Instead of sending the entire document to the language model, the system retrieves the most relevant chunks and uses them as context.

---

## 🛠️ Tech Stack

### Backend

- Python
- FastAPI
- Pydantic

### RAG / AI

- Sentence Transformers
- `all-MiniLM-L6-v2`
- FAISS
- Google Gemini API

### Document Processing

- PyMuPDF
- LangChain Text Splitters

### Frontend

- Streamlit

### Development

- Git
- GitHub
- Python Virtual Environment

---

## 📁 Project Structure

```text
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
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ai-document-qa
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

### 3. Activate virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

The `.env` file is excluded from Git using `.gitignore`.

---

## ▶️ Running the Application

### Start FastAPI backend

```bash
python -m uvicorn app.main:app
```

Backend:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

### Start Streamlit frontend

Open another terminal:

```bash
streamlit run app/ui/streamlit_app.py
```

Streamlit:

```text
http://localhost:8501
```

---

## 🔌 API Endpoints

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

### Upload Document

```http
POST /upload
```

Uploads and processes a PDF document.

The pipeline extracts text, creates chunks, generates embeddings, and adds them to the FAISS vector store.

### Ask Question

```http
POST /ask
```

Request:

```json
{
  "question": "What skills are mentioned in the document?"
}
```

Response:

```json
{
  "answer": "The document mentions Python, SQL...",
  "sources": []
}
```

---

## 🔍 Retrieval Process

The system uses:

```text
all-MiniLM-L6-v2
        ↓
384-dimensional embeddings
        ↓
FAISS IndexFlatL2
        ↓
Top 3 relevant chunks
```

The retrieved chunks are combined into the context provided to Gemini.

---

## 📚 Multiple Documents

The application supports adding multiple PDF documents to the same vector store.

For each uploaded document:

```text
PDF
 ↓
Chunks
 ↓
Embeddings
 ↓
Existing FAISS Index
 ↓
Add new vectors
 ↓
Updated Vector Store
```

Each chunk also stores its source filename so retrieved content can be traced back to the document it came from.

---

## 🛡️ Basic Error Handling

The application handles cases such as:

- Backend unavailable
- Request timeout
- Empty PDF
- PDF without readable text
- Missing vector store
- Missing chunk data
- Invalid user question

---

## 🎯 Project Goal

The goal of this project is to demonstrate a practical implementation of a **Retrieval-Augmented Generation system** rather than relying on a language model alone.

It combines:

- Document processing
- Natural language embeddings
- Vector databases
- Semantic retrieval
- Large Language Models
- REST APIs
- Web application development

---

## 🔮 Future Improvements

Potential future improvements include:

- Document deletion and management
- Chat history
- Better source citations
- Streaming LLM responses
- Authentication
- Improved retrieval techniques
- Reranking retrieved documents
- Metadata filtering
- Production deployment
- Automated testing
- Docker-based deployment

---

## 👨‍💻 Author

**Prem Shinde**

Computer Engineering Graduate

Interested in:

- Python Development
- AI/ML
- Data Science
- Backend Development
- RAG & LLM Applications

---

## ⭐ Project

If you find this project useful, consider giving it a star on GitHub.
```

### Ek important correction

README mein **`data/` structure dikhana okay hai**, but actual PDF/FAISS files `.gitignore` ki wajah se GitHub par nahi jayengi.

Ab:

```bash
git add README.md
git commit -m "docs: improve project README"
git push origin main
```

