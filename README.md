
```markdown
# 📚 AI Document Q&A — RAG Knowledge Assistant

An AI-powered document question-answering system built using **Retrieval-Augmented Generation (RAG)**.

The application allows users to upload PDF documents and ask questions about their content. Relevant document chunks are retrieved using semantic search and provided to a Gemini language model to generate grounded answers with source references.

---

## 🚀 Features

- 📄 Upload PDF documents
- 📝 Extract text from PDF files
- ✂️ Split documents into smaller chunks
- 🧠 Generate embeddings using Sentence Transformers
- 🔎 Semantic similarity search using FAISS
- 📚 Support for multiple PDF documents
- 🏷️ Track source documents for retrieved content
- 🤖 Generate answers using Google Gemini
- 🌐 FastAPI REST API backend
- 🎨 Streamlit web interface
- 💾 Persistent FAISS vector store
- ⚠️ Basic error handling

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
```

---

## 🧠 How RAG Works

The application uses two main pipelines.

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
```

Instead of sending the complete document to the language model, the system retrieves the most relevant chunks and provides only that context to the model.

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

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

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

The application uses two processes: a FastAPI backend and a Streamlit frontend.

### Start FastAPI Backend

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

### Start Streamlit Frontend

Open another terminal and run:

```bash
streamlit run app/ui/streamlit_app.py
```

Application:

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

The document is:

1. Saved locally
2. Parsed into text
3. Split into chunks
4. Converted into embeddings
5. Added to the FAISS vector store

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

The application uses the following retrieval pipeline:

```text
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
```

The retrieved chunks are combined into the context provided to the language model.

---

## 📚 Multiple Document Support

The system supports adding multiple PDF documents to the same vector store.

For each uploaded document:

```text
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
```

Each chunk stores the source filename, allowing retrieved content to be traced back to the original document.

---

## 🛡️ Error Handling

The application includes basic handling for:

- Backend connection failures
- Request timeouts
- Empty PDF files
- PDFs without readable text
- Missing vector store
- Missing chunk data
- Invalid questions
- API errors

---

## 🎯 Project Objective

The objective of this project is to build a practical **Retrieval-Augmented Generation system** that combines document retrieval with a large language model.

The project demonstrates practical implementation of:

- Document processing
- Text chunking
- Text embeddings
- Vector databases
- Semantic search
- Retrieval-Augmented Generation
- Large Language Models
- REST APIs
- Web application development

---

## 🔮 Future Improvements

- Document deletion and management
- Chat history
- Improved source citations
- Streaming LLM responses
- User authentication
- Metadata filtering
- Retrieval reranking
- Hybrid search
- Automated testing
- Dockerization
- Cloud deployment

---

## 👨‍💻 Author

**Prem Shinde**

Computer Engineering Graduate

### Areas of Interest

- Python Development
- AI / ML
- Data Science
- Backend Development
- RAG & LLM Applications

---

## ⭐ Project

If you find this project useful, consider giving the repository a star on GitHub.
```

Bas **`README.md` mein pura replace karke save** kar. Then:

```bash
git add README.md
git commit -m "docs: improve project README"
git push origin main
```
