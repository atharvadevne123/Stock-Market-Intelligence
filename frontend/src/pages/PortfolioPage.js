import React, { useState } from 'react';
import axios from 'axios';

function PortfolioPage() {
  const [tickers, setTickers] = useState('AAPL,MSFT,GOOGL');
  const [portfolio, setPortfolio] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzePortfolio = async () => {
    setLoading(true);
    try {
      const response = await axios.get(
        `http://localhost:8000/api/portfolio?tickers=${tickers}`
      );
      setPortfolio(response.data);
    } catch (error) {
      console.error('Error analyzing portfolio:', error);
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1 className="section-title">Portfolio Analysis</h1>

      <div className="search-box">
        <input
          type="text"
          value={tickers}
          onChange={(e) => setTickers(e.target.value)}
          placeholder="Enter tickers separated by comma"
          className="search-input"
        />
        <button onClick={analyzePortfolio} className="button">
          Analyze Portfolio
        </button>
      </div>

      {loading && <div className="loading">Analyzing portfolio...</div>}

      {portfolio && (
        <div className="card">
          <h2>Recommendation: {portfolio.summary?.recommendation}</h2>
          <div style={{ marginTop: '20px' }}>
            <p>BUY Signals: {portfolio.summary?.signal_distribution?.BUY}</p>
            <p>SELL Signals: {portfolio.summary?.signal_distribution?.SELL}</p>
            <p>HOLD Signals: {portfolio.summary?.signal_distribution?.HOLD}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default PortfolioPage;
