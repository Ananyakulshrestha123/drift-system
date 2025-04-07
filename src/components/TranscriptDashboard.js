import { useState, useEffect } from "react";
import axios from "axios";
import { useLocation } from "react-router-dom";
import "./TranscriptDashboard.css";

function TranscriptDashboard() {
  const location = useLocation();
  const [transcript, setTranscript] = useState(location.state?.transcript || "");
  const [allTranscripts, setAllTranscripts] = useState([]);
  const [showSummary, setShowSummary] = useState(false);

  const fetchTranscripts = async () => {
    try {
      const res = await axios.get("http://localhost:5000/transcripts");
      setAllTranscripts(res.data);
    } catch (err) {
      console.error("Error fetching transcripts:", err);
    }
  };

  useEffect(() => {
    fetchTranscripts();
  }, []);

  const generateSummary = () => {
    setShowSummary(true);
  };

  return (
    <div className="dashboard-container">
      <h2>📝 Transcript Dashboard</h2>

      {transcript && (
        <div className="transcript-box">
          <h3>Meeting Transcript</h3>
          <p>{transcript}</p>
          <button className="upload-btn" onClick={generateSummary}>Generate Summary</button>
        </div>
      )}

      {showSummary && (
        <div className="summary-box">
          <h3>📌 Meeting Summary</h3>
          <p>Summary feature coming soon...</p>
        </div>
      )}

      <div className="all-transcripts">
        <h3>📋 All Transcripts</h3>
        {allTranscripts.length === 0 ? (
          <p>No transcripts found.</p>
        ) : (
          allTranscripts.map((t, idx) => (
            <div className="transcript-card" key={idx}>
              <p><strong>Transcript:</strong></p>
              <div className="transcript-text">{t.transcript}</div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default TranscriptDashboard;
