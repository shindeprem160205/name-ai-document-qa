import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);

  // PDF select
  function handleFileChange(event) {
    setFile(event.target.files[0]);
    setUploadMessage("");
  }

  // Upload PDF to FastAPI
  async function handleUpload() {
    if (!file) {
      setUploadMessage("Please select a PDF first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setUploadMessage("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (response.ok) {
        setUploadMessage(
          `Uploaded successfully. ${data.chunks} chunks created.`
        );
      } else {
        setUploadMessage(data.detail || "Upload failed.");
      }
    } catch (error) {
      console.error(error);
      setUploadMessage("Could not connect to the backend.");
    } finally {
      setLoading(false);
    }
  }

  // Ask question
  async function handleAsk() {
    if (!question.trim()) {
      setAnswer("Please enter a question.");
      return;
    }

    setLoading(true);
    setAnswer("");
    setSources([]);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/ask",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: question,
          }),
        }
      );

      const data = await response.json();

      if (response.ok) {
        setAnswer(data.answer);
        setSources(data.sources || []);
      } else {
        setAnswer(data.detail || "Something went wrong.");
      }
    } catch (error) {
      console.error(error);
      setAnswer("Could not connect to the backend.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1>AI Document Q&A</h1>

      <p>
        Upload a PDF and ask questions about its content.
      </p>

      {/* Upload Section */}
      <section>
        <h2>Upload Document</h2>

        <input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
        />

        {file && (
          <p>
            Selected file: <strong>{file.name}</strong>
          </p>
        )}

        <button onClick={handleUpload} disabled={loading}>
          {loading ? "Processing..." : "Upload PDF"}
        </button>

        {uploadMessage && (
          <p>{uploadMessage}</p>
        )}
      </section>

      <hr />

      {/* Question Section */}
      <section>
        <h2>Ask a Question</h2>

        <input
          type="text"
          placeholder="What are the global logistics trends?"
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
        />

        <button onClick={handleAsk} disabled={loading}>
          {loading ? "Thinking..." : "Ask"}
        </button>
      </section>

      {/* Answer Section */}
      {answer && (
        <section>
          <h2>Answer</h2>

          <p>{answer}</p>
        </section>
      )}

      {/* Sources Section */}
      {sources.length > 0 && (
        <section>
          <h2>Sources</h2>

          {sources.map((source, index) => (
            <div key={index}>
              <h3>Source {index + 1}</h3>
              <p>{source}</p>
            </div>
          ))}
        </section>
      )}
    </div>
  );
}

export default App;