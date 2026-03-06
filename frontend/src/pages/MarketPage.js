import React, { useState, useEffect } from 'react';
import axios from 'axios';

function MarketPage() {
  const [market, setMarket] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMarketOverview = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/market/overview');
        setMarket(response.data);
      } catch (error) {
        console.error('Error fetching market overview:', error);
      }
      setLoading(false);
    };

    fetchMarketOverview();
  }, []);

  return (
    <div className="container">
      <h1 className="section-title">Market Overview</h1>

      {loading && <div className="loading">Loading market data...</div>}

      {market && (
        <div className="card">
          <h2>Market Trend: {market.market_trend}</h2>
          <div style={{ marginTop: '20px' }}>
            <p>Articles Analyzed: {market.articles_analyzed}</p>
            <p>Positive: {(market.sentiment_ratios?.positive * 100).toFixed(1)}%</p>
            <p>Negative: {(market.sentiment_ratios?.negative * 100).toFixed(1)}%</p>
            <p>Neutral: {(market.sentiment_ratios?.neutral * 100).toFixed(1)}%</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default MarketPage;
