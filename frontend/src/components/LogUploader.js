import React, { useState } from 'react';
import axios from 'axios';
import './LogUploader.js';

function LogUploader({ onSummary }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const response = await axios.post("http://localhost:8000/api/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });
      onSummary(response.data.summary);
    } catch (error) {
      console.error("Error uploading file:", error);
      onSummary("Error processing log file.");
    }
    setLoading(false);
  };

  return (
    <div className="log-uploader">
      <input type="file" accept=".txt" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Processing..." : "Upload and Summarize"}
      </button>
    </div>
  );
}

export default LogUploader;