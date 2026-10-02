import requests
import streamlit as st


# -----------------------------
# Configuration
# -----------------------------

BACKEND_URL = "http://127.0.0.1:8000"


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
            margin-bottom: 5px;
        }

        .subtitle {
            font-size: 18px;
            color: #777;
            margin-bottom: 30px;
        }

        .answer-box {
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #ddd;
            margin-top: 15px;
        }

        .source-box {
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #ddd;
            margin-bottom: 10px;
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
    'Upload a PDF and ask questions using Retrieval-Augmented Generation.'
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
        "Upload a PDF",
        type=["pdf"]
    )

    if uploaded_file:

        st.write(
            f"**Selected:** {uploaded_file.name}"
        )

        if st.button(
            "🚀 Process Document",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "Processing document..."
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
                    st.session_state.filename = (
                        data.get("filename", uploaded_file.name)
                    )

                    st.success(
                        "Document processed successfully!"
                    )

                    st.info(
                        f"Created {data.get('chunks', 0)} chunks."
                    )

                else:

                    st.error(
                        f"Upload failed: {response.text}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to FastAPI backend."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "Processing took too long. Please try again."
                )

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )


# -----------------------------
# Main Question Area
# -----------------------------

st.header("💬 Ask a Question")

if st.session_state.uploaded:

    st.success(
        f"📄 Active document: {st.session_state.filename}"
    )

else:

    st.info(
        "Upload and process a PDF from the sidebar first."
    )


question = st.text_area(
    "Your question",
    placeholder=(
        "Example: What are the global logistics trends?"
    ),
    height=100
)


if st.button(
    "🔍 Ask Question",
    type="primary",
    use_container_width=True
):

    if not st.session_state.uploaded:

        st.warning(
            "Please upload and process a PDF first."
        )

    elif not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        try:

            with st.spinner(
                "Searching the document and generating answer..."
            ):

                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    json={
                        "question": question
                    },
                    timeout=120
                )

            if response.status_code == 200:

                data = response.json()

                st.session_state.answer = (
                    data.get("answer", "")
                )

                st.session_state.sources = (
                    data.get("sources", [])
                )

            else:

                st.error(
                    f"Request failed: {response.text}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI backend."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The request timed out. Please try again."
            )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )


# -----------------------------
# Answer
# -----------------------------

if st.session_state.answer:

    st.divider()

    st.header("🤖 Answer")

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

if st.session_state.sources:

    st.header("📚 Sources")

    for index, source in enumerate(
        st.session_state.sources,
        start=1
    ):

        with st.expander(
            f"Source {index}"
        ):

            st.write(source)