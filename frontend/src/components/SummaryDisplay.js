import React from 'react';
import ReactMarkdown from 'react-markdown';
import './SummaryDisplay.css';

function SummaryDisplay({ summary }) {
  return (
    <div className="summary-display">
      <h2>Summary</h2>
      <ReactMarkdown children={summary} />
    </div>
  );
}

export default SummaryDisplay;