import React, { useState } from 'react';
import Layout from '../components/Layout';

const SignalsPage = () => {
  const [selectedTicker, setSelectedTicker] = useState('TSLA');

  const newsCards = [
    {
      sentiment: 0.88,
      source: 'Reddit / r/wallstreetbets',
      sourceIcon: 'forum',
      time: '12m ago',
      ticker: 'TSLA',
      title: 'Tesla expansion into Southeast Asia markets confirms bullish delivery projections for Q4.',
      tags: ['#expansion', '#southeast-asia', '#logistics'],
      sentimentLabel: 'BULLISH',
    },
    {
      sentiment: -0.42,
      source: 'Bloomberg Intelligence',
      sourceIcon: 'newspaper',
      time: '45m ago',
      ticker: 'US10Y',
      title: 'Treasury yields spike following hawkish commentary from Federal Reserve regional presidents.',
      tags: ['#fixed-income', '#inflation'],
      sentimentLabel: 'BEARISH',
    },
    {
      sentiment: 0.05,
      source: 'Reuters Market Signal',
      sourceIcon: 'language',
      time: '1h ago',
      ticker: 'M&A',
      title: 'Major pharmaceutical conglomerate enters quiet period, sparking merger speculation across biotech sector.',
      tags: ['#biotech', '#mergers', '#insider-flow'],
      sentimentLabel: 'NEUTRAL',
    },
    {
      sentiment: 0.92,
      source: 'On-Chain Analytics',
      sourceIcon: 'currency_bitcoin',
      time: '3h ago',
      ticker: 'BTC',
      title: 'Institutional whale accumulation hits 2-year high as spot ETF net inflows accelerate.',
      tags: ['#institutional-flow', '#whales'],
      sentimentLabel: 'BULLISH',
    },
  ];

  return (
    <Layout>
      <main className="flex gap-8">
        {/* Sidebar Filter */}
        <aside className="w-72 flex-shrink-0 space-y-6">
          <div className="bg-surface-container-low rounded-xl p-6 border border-outline-variant/10">
            <h3 className="font-headline text-sm font-bold uppercase tracking-widest mb-6 flex items-center gap-2">
              <span className="material-symbols-outlined text-primary text-lg">filter_list</span>
              Signal Filters
            </h3>
            <div className="space-y-6">
              {/* Tickers */}
              <div>
                <label className="text-[10px] font-bold text-on-surface-variant uppercase tracking-tighter block mb-3">
                  Ticker Universe
                </label>
                <div className="flex flex-wrap gap-2">
                  {['TSLA', 'NVDA', 'BTC', 'AAPL'].map((ticker) => (
                    <button
                      key={ticker}
                      onClick={() => setSelectedTicker(ticker)}
                      className={`px-2 py-1 rounded text-[10px] font-bold border transition-all ${
                        selectedTicker === ticker
                          ? 'bg-surface-container-high text-primary border-primary/20'
                          : 'bg-surface-container-lowest text-on-surface-variant border-outline-variant/10 hover:border-primary/40'
                      }`}
                    >
                      {ticker}
                    </button>
                  ))}
                </div>
              </div>

              {/* Sentiment */}
              <div>
                <label className="text-[10px] font-bold text-on-surface-variant uppercase tracking-tighter block mb-3">
                  Sentiment Threshold
                </label>
                <div className="space-y-2">
                  {[
                    { label: 'Highly Positive (>0.8)', checked: true },
                    { label: 'Market Neutral', checked: false },
                    { label: 'Contrarian/Negative', checked: false },
                  ].map((item, i) => (
                    <label key={i} className="flex items-center gap-3 cursor-pointer group">
                      <input
                        type="checkbox"
                        defaultChecked={item.checked}
                        className="rounded-sm bg-surface-container-lowest border-outline-variant/20 text-primary focus:ring-0 focus:ring-offset-0"
                      />
                      <span className="text-xs text-on-surface group-hover:text-primary transition-colors">
                        {item.label}
                      </span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Sources */}
              <div>
                <label className="text-[10px] font-bold text-on-surface-variant uppercase tracking-tighter block mb-3">
                  Data Sources
                </label>
                <div className="space-y-3">
                  {[
                    { name: 'Reddit', color: 'text-[#ff4500]', status: 'Active' },
                    { name: 'Bloomberg', color: 'text-[#0077b5]', status: 'Active' },
                    { name: 'Reuters', color: 'text-on-surface-variant', status: 'Paused' },
                  ].map((source, i) => (
                    <div key={i} className="flex items-center justify-between text-xs p-2 rounded bg-surface-container-lowest border border-outline-variant/5">
                      <span className="flex items-center gap-2">
                        <span className="material-symbols-outlined text-sm">forum</span> {source.name}
                      </span>
                      <span className={`text-[10px] ${source.status === 'Active' ? 'text-primary' : 'text-on-surface-variant'}`}>
                        {source.status}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Scraping Status Widget */}
          <div className="bg-surface-container-lowest rounded-xl p-5 border border-primary/10 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-primary/5 rounded-full -mr-16 -mt-16 blur-3xl"></div>
            <h4 className="text-[10px] font-bold text-primary uppercase tracking-widest mb-4 flex items-center gap-2">
              <span className="w-1.5 h-1.5 bg-primary rounded-full animate-pulse"></span>
              Engine: Live Scraping
            </h4>
            <div className="flex items-end justify-between mb-4">
              <div>
                <p className="text-2xl font-headline font-extrabold text-on-surface leading-none">15.8</p>
                <p className="text-[10px] text-on-surface-variant mt-1">Sources / Second</p>
              </div>
              <div className="flex gap-1 h-8 items-end">
                {[40, 60, 50, 80, 70].map((h, i) => (
                  <div key={i} className="w-1 bg-primary/80 rounded-t" style={{ height: `${h / 100 * 32}px` }}></div>
                ))}
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between text-[10px]">
                <span className="text-on-surface-variant">Queue Depth</span>
                <span className="text-on-surface font-mono">1.2k req</span>
              </div>
              <div className="w-full bg-surface-container-highest h-1 rounded-full overflow-hidden">
                <div className="bg-primary h-full w-[65%]"></div>
              </div>
            </div>
          </div>
        </aside>

        {/* News Feed Canvas */}
        <section className="flex-1 space-y-6 max-w-4xl">
          {/* Feed Header */}
          <div className="flex justify-between items-center mb-8">
            <div>
              <h2 className="font-headline text-2xl font-extrabold tracking-tight">
                Market Intelligence Feed
              </h2>
              <p className="text-sm text-on-surface-variant">Analyzing 12,482 headlines using FinBERT v4.2</p>
            </div>
            <div className="flex gap-2">
              <button className="p-2 rounded bg-surface-container-low text-on-surface-variant hover:text-primary transition-colors">
                <span className="material-symbols-outlined">refresh</span>
              </button>
              <button className="p-2 rounded bg-surface-container-low text-on-surface-variant hover:text-primary transition-colors">
                <span className="material-symbols-outlined">sort</span>
              </button>
            </div>
          </div>

          {/* News Cards */}
          {newsCards.map((card, i) => (
            <div
              key={i}
              className="bg-surface-container-low rounded-xl border border-outline-variant/10 p-6 hover:bg-surface-container hover:border-primary/20 transition-all cursor-pointer group"
            >
              <div className="flex gap-6">
                {/* FinBERT Score Visual */}
                <div className="flex flex-col items-center gap-2 min-w-fit">
                  <div className="relative w-12 h-12 flex items-center justify-center">
                    <svg className="w-full h-full -rotate-90">
                      <circle cx="24" cy="24" fill="none" r="20" stroke="#2d3449" strokeWidth="4"></circle>
                      <circle
                        cx="24"
                        cy="24"
                        fill="none"
                        r="20"
                        stroke={card.sentiment > 0 ? '#4edea3' : '#ffb2b7'}
                        strokeDasharray="125"
                        strokeDashoffset={125 - Math.abs(card.sentiment) * 125}
                        strokeWidth="4"
                      ></circle>
                    </svg>
                    <span className="absolute text-[10px] font-bold text-primary">{card.sentiment.toFixed(2)}</span>
                  </div>
                  <span className="text-[9px] font-bold uppercase tracking-tighter text-on-surface-variant">
                    Sentiment
                  </span>
                </div>

                <div className="flex-1">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-3">
                      <div className="flex items-center gap-1 bg-surface-container-lowest px-2 py-0.5 rounded border border-outline-variant/10">
                        <span className="material-symbols-outlined text-[14px]">{card.sourceIcon}</span>
                        <span className="text-[10px] font-bold text-on-surface-variant uppercase">
                          {card.source}
                        </span>
                      </div>
                      <span className="text-[10px] text-on-surface-variant/60">{card.time}</span>
                    </div>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-widest border ${
                      card.sentimentLabel === 'BULLISH'
                        ? 'bg-primary-container text-primary border-primary/20'
                        : card.sentimentLabel === 'BEARISH'
                        ? 'bg-secondary-container/20 text-secondary border-secondary/20'
                        : 'bg-surface-container-highest text-on-surface-variant'
                    }`}>
                      {card.ticker}
                    </span>
                  </div>
                  <h3 className="text-lg font-headline font-bold text-on-surface mb-3 group-hover:text-primary transition-colors">
                    {card.title}
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {card.tags.map((tag, j) => (
                      <span key={j} className="text-[10px] px-2 py-0.5 bg-surface-container-highest rounded-full text-on-surface-variant">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))}

          {/* Loading More Utility */}
          <div className="pt-8 text-center">
            <button className="px-6 py-2 rounded-full border border-outline-variant/20 text-on-surface-variant text-xs font-bold uppercase tracking-widest hover:bg-surface-container-high transition-colors">
              Load Historical Signals
            </button>
          </div>
        </section>

        {/* Right Status Rail */}
        <aside className="w-64 space-y-6">
          <div className="bg-surface-container-low rounded-xl p-4 border border-outline-variant/10">
            <h5 className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest mb-4">
              Sentiment Divergence
            </h5>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-xs">Social Sentiment</span>
                <span className="text-xs text-primary font-bold">+78%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-xs">Institutional Sentiment</span>
                <span className="text-xs text-secondary font-bold">-12%</span>
              </div>
              <div className="mt-4 pt-4 border-t border-outline-variant/10">
                <p className="text-[9px] text-on-surface-variant italic leading-relaxed">
                  System Note: High divergence often precedes volatility expansion. Monitoring for breakout.
                </p>
              </div>
            </div>
          </div>

          <div className="bg-surface-container-low rounded-xl p-4 border border-outline-variant/10 overflow-hidden relative">
            <div className="absolute bottom-0 right-0 p-1 opacity-10">
              <span className="material-symbols-outlined text-4xl">hub</span>
            </div>
            <h5 className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest mb-4">
              FinBERT Latency
            </h5>
            <div className="flex items-baseline gap-1">
              <span className="text-xl font-headline font-bold text-primary">12ms</span>
              <span className="text-[10px] text-on-surface-variant">Inference</span>
            </div>
            <div className="mt-4 h-12 flex items-end gap-1">
              {[60, 70, 40, 90, 50].map((h, i) => (
                <div
                  key={i}
                  className="flex-1 bg-primary/40 rounded-t-sm"
                  style={{ height: `${h / 100 * 48}px` }}
                ></div>
              ))}
            </div>
          </div>
        </aside>
      </main>
    </Layout>
  );
};

export default SignalsPage;
