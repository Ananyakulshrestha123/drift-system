import React, { useState } from "react";
import axios from "axios";

function AudioUploader() {
  const [file, setFile] = useState(null);
  const [transcript, setTranscript] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      const response = await axios.post("http://localhost:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setTranscript(response.data.transcript);
    } catch (error) {
      console.error("Transcription failed:", error);
      alert("Transcription failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 max-w-xl mx-auto mt-10 shadow-md rounded-xl border">
      <h2 className="text-xl font-bold mb-4">🎤 Upload Audio for Transcription</h2>
      <input type="file" accept="audio/*" onChange={handleFileChange} className="mb-4" />
      <br />
      <button
        onClick={handleUpload}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        disabled={loading}
      >
        {loading ? "Transcribing..." : "Upload & Transcribe"}
      </button>

      {transcript && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold mb-2">📝 Transcript:</h3>
          <p className="whitespace-pre-line bg-gray-100 p-4 rounded">{transcript}</p>
        </div>
      )}
    </div>
  );
}

export default AudioUploader;
