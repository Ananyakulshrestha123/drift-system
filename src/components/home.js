import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./Home.css";

function Home() {
  const [file, setFile] = useState(null);
  const [transcript, setTranscript] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const uploadAudio = async () => {
    if (!file) {
      alert("Please select an audio file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      const res = await axios.post("http://localhost:5000/upload", formData);
      if (res.data.transcript) {
        const transcriptText = res.data.transcript;
        setTranscript(transcriptText);

        // Store transcript in MongoDB
        await axios.post(
          "http://localhost:5000/store_transcript",
          { transcript: transcriptText },
          { headers: { "Content-Type": "application/json" } }
        );
      } else {
        alert("Transcription failed: " + (res.data.error || "Unknown error"));
      }
    } catch (err) {
      alert("Upload error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const goToTranscriptDashboard = () => {
    navigate("/TranscriptDashboard", {
      state: { transcript },
    });
  };

  return (
    <div className="home-container">
      <h2>🎧 Upload Your Audio</h2>
      <input
        type="file"
        accept="audio/*"
        className="file-input"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button className="upload-btn" onClick={uploadAudio} disabled={loading}>
        {loading ? "Transcribing..." : "Upload & Transcribe"}
      </button>

      {transcript && (
        <div className="transcript-box">
          <h3>📝 Transcript</h3>
          <p>{transcript}</p>
          <button className="generate-btn" onClick={goToTranscriptDashboard}>
            Generate Summary
          </button>
        </div>
      )}
    </div>
  );
}

export default Home;
