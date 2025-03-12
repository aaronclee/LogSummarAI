import React, { useState } from 'react';
import LogUploader from './components/LogUploader';
import SummaryDisplay from './components/SummaryDisplay';
import './App.css';

function App() {
  const [summary, setSummary] = useState("");

  const handleSummary = (data) => {
    setSummary(data);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>LogSummarAI</h1>
      </header>
      <main>
        <LogUploader onSummary={handleSummary} />
        {summary && <SummaryDisplay summary={summary} />}
      </main>
    </div>
  );
}

export default App;