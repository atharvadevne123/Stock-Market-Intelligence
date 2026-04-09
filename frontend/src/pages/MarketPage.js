import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Layout from '../components/Layout';

function MarketPage() {
  const [market, setMarket] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchMarketOverview = async () => {
      setLoading(true);
      try {
        const response = await axios.get('http://localhost:8000/api/market/overview');
        setMarket(response.data);
      } catch (error) {
        console.error('Error fetching market overview:', error);
      }
      setLoading(false);
    };

    // Uncomment when backend is available
    // fetchMarketOverview();
  }, []);

  // Demo data when no backend available
  const demoMarket = market || {
    market_trend: 'BULLISH',
    articles_analyzed: 12482,
    sentiment_ratios: { positive: 0.68, negative: 0.18, neutral: 0.14 }
  };

  return (
    <Layout>
      {/* Hero Section: Market Overview */}
      <div className="grid grid-cols-12 gap-6 mb-8">
        <div className="col-span-12 lg:col-span-8 bg-surface-container-low rounded-xl p-8 relative overflow-hidden shadow-2xl">
          <div className="absolute top-0 right-0 p-8 opacity-10">
            <span className="material-symbols-outlined text-9xl">trending_up</span>
          </div>
          <div className="relative z-10">
            <h2 className="text-on-surface-variant text-sm font-label uppercase tracking-widest mb-2">
              Market Status
            </h2>
            <div className="flex items-end gap-4 mb-6">
              <span className="font-headline text-6xl font-extrabold text-on-surface leading-none">
                {demoMarket.market_trend}
              </span>
              <div className="mb-2 px-2 py-1 bg-primary/10 border border-primary/20 text-primary rounded text-xs font-bold tracking-tighter">
                {demoMarket.articles_analyzed.toLocaleString()} ARTICLES
              </div>
            </div>
            <div className="grid grid-cols-3 gap-8">
              <div>
                <p className="text-[10px] uppercase text-outline mb-1">Positive Sentiment</p>
                <div className="h-1.5 w-full bg-surface-container-highest rounded-full overflow-hidden">
                  <div className="h-full bg-primary w-[68%] shadow-[0_0_8px_rgba(78,222,163,0.5)]"></div>
                </div>
                <span className="text-sm font-bold text-primary mt-1">{(demoMarket.sentiment_ratios.positive * 100).toFixed(1)}%</span>
              </div>
              <div>
                <p className="text-[10px] uppercase text-outline mb-1">Neutral Sentiment</p>
                <div className="h-1.5 w-full bg-surface-container-highest rounded-full overflow-hidden">
                  <div className="h-full bg-tertiary w-[14%]"></div>
                </div>
                <span className="text-sm font-bold text-tertiary mt-1">{(demoMarket.sentiment_ratios.neutral * 100).toFixed(1)}%</span>
              </div>
              <div>
                <p className="text-[10px] uppercase text-outline mb-1">Negative Sentiment</p>
                <div className="h-1.5 w-full bg-surface-container-highest rounded-full overflow-hidden">
                  <div className="h-full bg-secondary w-[18%]"></div>
                </div>
                <span className="text-sm font-bold text-secondary mt-1">{(demoMarket.sentiment_ratios.negative * 100).toFixed(1)}%</span>
              </div>
            </div>
          </div>
        </div>
        <div className="col-span-12 lg:col-span-4 bg-surface-container-low rounded-xl p-6 border border-outline-variant/10 flex flex-col justify-between">
          <div>
            <h3 className="text-on-surface font-headline font-bold text-lg mb-4">Market Metrics</h3>
            <div className="space-y-4">
              <div className="p-4 bg-surface-container-lowest rounded border border-outline-variant/10">
                <p className="text-[10px] text-on-surface-variant uppercase font-bold mb-1">Articles Analyzed</p>
                <p className="text-2xl font-bold text-primary font-headline">{demoMarket.articles_analyzed.toLocaleString()}</p>
              </div>
              <div className="p-4 bg-surface-container-lowest rounded border border-outline-variant/10">
                <p className="text-[10px] text-on-surface-variant uppercase font-bold mb-1">Analysis Engine</p>
                <p className="text-lg font-bold text-on-surface">FinBERT v4.2</p>
                <p className="text-[10px] text-on-surface-variant mt-1">12ms Latency</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Sector Performance */}
      <div className="bg-surface-container-low rounded-xl border border-outline-variant/10 p-8 mb-8">
        <h2 className="font-headline font-bold text-2xl mb-6 text-on-surface">Sector Performance</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { name: 'Technology', change: '+2.4%', sentiment: 'Very Bullish' },
            { name: 'Healthcare', change: '-3.2%', sentiment: 'Bearish' },
            { name: 'Finance', change: '-0.4%', sentiment: 'Neutral' },
            { name: 'Energy', change: '+0.8%', sentiment: 'Neutral' },
            { name: 'Consumer', change: '+1.1%', sentiment: 'Bullish' },
            { name: 'Materials', change: '+0.2%', sentiment: 'Neutral' },
            { name: 'Industrials', change: '-1.1%', sentiment: 'Bearish' },
            { name: 'Utilities', change: '0.0%', sentiment: 'Neutral' },
          ].map((sector, i) => (
            <div key={i} className="p-4 bg-surface-container-highest rounded-lg border border-outline-variant/10">
              <h4 className="text-sm font-bold text-on-surface mb-2">{sector.name}</h4>
              <p className={`text-lg font-bold font-headline ${sector.change.startsWith('+') ? 'text-primary' : 'text-secondary'}`}>
                {sector.change}
              </p>
              <p className="text-[10px] text-on-surface-variant mt-2">{sector.sentiment}</p>
            </div>
          ))}
        </div>
      </div>

      {loading && (
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary mb-4"></div>
            <p className="text-on-surface-variant">Loading market data...</p>
          </div>
        </div>
      )}
    </Layout>
  );
}

export default MarketPage;
