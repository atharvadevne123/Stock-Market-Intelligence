import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Dashboard.css';
import SignalCard from './SignalCard';

function Dashboard() {
  const [signal, setSignal] = useState(null);
  const [loading, setLoading] = useState(false);
  const [ticker, setTicker] = useState('AAPL');

  const analyzeStock = async () => {
    setLoading(true);
    try {
      const response = await axios.get(
        `http://localhost:8000/api/analyze/${ticker}`
      );
      setSignal(response.data);
    } catch (error) {
      console.error('Error analyzing stock:', error);
    }
    setLoading(false);
  };

  useEffect(() => {
    analyzeStock();
  }, []);

  return (
    <div className="dashboard">
      <div className="container">
        <h1 className="section-title">Stock Analysis Dashboard</h1>

        <div className="search-box">
          <input
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value.toUpperCase())}
            placeholder="Enter ticker symbol"
            className="search-input"
          />
          <button onClick={analyzeStock} className="button search-button">
            Analyze
          </button>
        </div>

        {loading && <div className="loading">Loading analysis...</div>}

        {signal && <SignalCard signal={signal} />}
      </div>
    </div>
  );
}

export default Dashboard;
