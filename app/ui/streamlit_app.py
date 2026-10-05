import requests
import streamlit as st


# -----------------------------
# Configuration
# -----------------------------

import os
import streamlit as st
import requests

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Document Q&A",
    page_icon="📚",
    layout="wide"
)


# -----------------------------
# Custom CSS
# -----------------------------

st.markdown(
    """
    <style>

        .main-title {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 4px;
        }

        .subtitle {
            font-size: 17px;
            color: #777;
            margin-bottom: 25px;
        }

        .answer-box {
            padding: 22px;
            border-radius: 12px;
            border: 1px solid #ddd;
            background-color: #fafafa;
            line-height: 1.7;
            font-size: 16px;
        }

        .document-card {
            padding: 16px;
            border-radius: 12px;
            border: 1px solid #ddd;
            margin-bottom: 15px;
        }

        .source-box {
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #ddd;
            margin-bottom: 10px;
            line-height: 1.6;
        }

        .section-title {
            font-size: 25px;
            font-weight: 650;
            margin-top: 10px;
        }

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Header
# -----------------------------

st.markdown(
    '<div class="main-title">📚 AI Document Q&A</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Ask questions about your documents using Retrieval-Augmented Generation (RAG).'
    '</div>',
    unsafe_allow_html=True
)


# -----------------------------
# Session State
# -----------------------------

if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

if "filename" not in st.session_state:
    st.session_state.filename = ""

if "chunks" not in st.session_state:
    st.session_state.chunks = 0

if "answer" not in st.session_state:
    st.session_state.answer = ""

if "sources" not in st.session_state:
    st.session_state.sources = []


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.header("📄 Document")

    uploaded_file = st.file_uploader(
        "Upload a PDF document",
        type=["pdf"],
        help="Upload a PDF to build the document knowledge base."
    )

    if uploaded_file:

        st.markdown(
            f"""
            <div class="document-card">
                <strong>Selected document</strong><br>
                {uploaded_file.name}
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "🚀 Process Document",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "Extracting text, creating embeddings and building vector store..."
                ):

                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf"
                        )
                    }

                    response = requests.post(
                        f"{BACKEND_URL}/upload",
                        files=files,
                        timeout=300
                    )

                if response.status_code == 200:

                    data = response.json()

                    st.session_state.uploaded = True

                    st.session_state.filename = data.get(
                        "filename",
                        uploaded_file.name
                    )

                    st.session_state.chunks = data.get(
                        "chunks",
                        0
                    )

                    # Clear previous answer
                    st.session_state.answer = ""
                    st.session_state.sources = []

                    st.success(
                        "✅ Document processed successfully!"
                    )

                    st.info(
                        f"📦 {st.session_state.chunks} chunks created."
                    )

                else:

                    st.error(
                        f"Upload failed: {response.text}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Cannot connect to FastAPI backend. "
                    "Make sure the backend is running."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "⏳ Processing took too long. Please try again."
                )

            except Exception as e:

                st.error(
                    f"❌ Error: {str(e)}"
                )


# -----------------------------
# Active Document
# -----------------------------

st.markdown(
    '<div class="section-title">💬 Ask a Question</div>',
    unsafe_allow_html=True
)

if st.session_state.uploaded:

    st.success(
        f"📄 Active document: **{st.session_state.filename}**"
    )

else:

    st.info(
        "Upload and process a PDF from the sidebar to start asking questions."
    )


# -----------------------------
# Question Input
# -----------------------------

question = st.text_area(
    "Your question",
    placeholder="Example: What skills does the candidate have?",
    height=100
)


# -----------------------------
# Ask Question
# -----------------------------

if st.button(
    "🔍 Ask Question",
    type="primary",
    use_container_width=True
):

    if not st.session_state.uploaded:

        st.warning(
            "⚠️ Please upload and process a PDF first."
        )

    elif not question.strip():

        st.warning(
            "⚠️ Please enter a question."
        )

    else:

        try:

            with st.spinner(
                "🔎 Searching document and generating answer..."
            ):

                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    json={
                        "question": question.strip()
                    },
                    timeout=120
                )

            if response.status_code == 200:

                data = response.json()

                st.session_state.answer = data.get(
                    "answer",
                    ""
                )

                st.session_state.sources = data.get(
                    "sources",
                    []
                )

            else:

                st.error(
                    f"❌ Request failed: {response.text}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Cannot connect to FastAPI backend."
            )

        except requests.exceptions.Timeout:

            st.error(
                "⏳ The request timed out. Please try again."
            )

        except Exception as e:

            st.error(
                f"❌ Error: {str(e)}"
            )


# -----------------------------
# Answer
# -----------------------------

if st.session_state.answer:

    st.divider()

    st.markdown(
        '<div class="section-title">🤖 Answer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="answer-box">
            {st.session_state.answer}
        </div>
        """,
        unsafe_allow_html=True
    )


# -----------------------------
# Sources
# -----------------------------

# -----------------------------
# Sources
# -----------------------------

if st.session_state.sources:

    st.markdown(
        '<div class="section-title">📚 Retrieved Sources</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "These passages were retrieved from the uploaded document "
        "and provided to the language model as context."
    )

    for index, source in enumerate(
        st.session_state.sources,
        start=1
    ):

        with st.expander(
            f"📄 Source {index}"
        ):

            st.caption(
                f"Source: {source['source']}"
            )

            st.write(
                source["text"]
            )