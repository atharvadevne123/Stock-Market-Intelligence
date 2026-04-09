import React from 'react';
import Layout from '../components/Layout';

const DashboardPage = () => {
  const signals = [
    { ticker: 'NVDA', name: 'Nvidia Corporation', price: '$822.45', change: '+4.2%', signal: 'STRONG_BUY', sentiment: 92, changeColor: 'text-primary' },
    { ticker: 'TSLA', name: 'Tesla, Inc.', price: '$162.10', change: '-3.1%', signal: 'STRONG_SELL', sentiment: 18, changeColor: 'text-secondary' },
    { ticker: 'AMD', name: 'Advanced Micro Devices', price: '$174.45', change: '+2.8%', signal: 'STRONG_BUY', sentiment: 76, changeColor: 'text-primary' },
    { ticker: 'AAPL', name: 'Apple Inc.', price: '$189.20', change: '0.0%', signal: 'WATCH', sentiment: 50, changeColor: 'text-outline' },
  ];

  const feedItems = [
    { time: '2 MINS AGO', sentiment: 0.98, title: 'Federal Reserve hint at potential rate stabilization by Q3.', tags: ['#MACRO', '#FED'], sentiment_label: 'POS' },
    { time: '12 MINS AGO', sentiment: -0.84, title: 'Supply chain disruptions reported in Southeast Asian chip manufacturing hubs.', tags: ['#SEMI', '#LOGISTICS'], sentiment_label: 'NEG' },
    { time: '45 MINS AGO', sentiment: 0.12, title: 'Earnings Preview: What to expect from upcoming Big Tech reports next week.', tags: ['#EARNINGS', '#TECH'], sentiment_label: 'NEU' },
    { time: '1 HOUR AGO', sentiment: 0.72, title: 'New clean energy subsidy bill gains traction in Congress.', tags: ['#ESG', '#POLICY'], sentiment_label: 'POS' },
  ];

  return (
    <Layout>
      {/* Hero Section: Market Pulse */}
      <section className="grid grid-cols-12 gap-6 mb-8">
        <div className="col-span-12 lg:col-span-8 bg-surface-container-low rounded-xl p-8 relative overflow-hidden shadow-2xl">
          <div className="absolute top-0 right-0 p-8 opacity-10">
            <span className="material-symbols-outlined text-9xl">monitoring</span>
          </div>
          <div className="relative z-10">
            <h2 className="text-on-surface-variant text-sm font-label uppercase tracking-widest mb-2">
              Market Pulse Index
            </h2>
            <div className="flex items-end gap-4 mb-6">
              <span className="font-headline text-6xl font-extrabold text-on-surface leading-none">
                84.2
              </span>
              <div className="mb-2 px-2 py-1 bg-primary/10 border border-primary/20 text-primary rounded text-xs font-bold tracking-tighter">
                EXTREME GREED
              </div>
            </div>
            <div className="grid grid-cols-3 gap-8">
              <div>
                <p className="text-[10px] uppercase text-outline mb-1">Global Sentiment</p>
                <div className="h-1.5 w-full bg-surface-container-highest rounded-full overflow-hidden">
                  <div className="h-full bg-primary w-[84%] shadow-[0_0_8px_rgba(78,222,163,0.5)]"></div>
                </div>
                <div className="flex justify-between text-[10px] mt-1 text-on-surface-variant/60">
                  <span>Fear</span>
                  <span>Greed</span>
                </div>
              </div>
              <div>
                <p className="text-[10px] uppercase text-outline mb-1">Buy/Sell Ratio</p>
                <div className="flex items-center gap-2">
                  <span className="text-primary font-headline font-bold">2.4x</span>
                  <span className="text-[10px] text-outline tracking-tight">Institutional Volume</span>
                </div>
              </div>
              <div>
                <p className="text-[10px] uppercase text-outline mb-1">Trend Velocity</p>
                <div className="flex items-center gap-2 text-primary">
                  <span className="material-symbols-outlined text-sm">trending_up</span>
                  <span className="font-headline font-bold">+12.4%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="col-span-12 lg:col-span-4 bg-surface-container-low rounded-xl p-6 border border-outline-variant/10 flex flex-col justify-between">
          <div>
            <h3 className="text-on-surface font-headline font-bold text-lg mb-4">Volatility Index</h3>
            <div className="aspect-video bg-surface-container-lowest rounded overflow-hidden relative">
              <div className="absolute inset-0 flex items-end">
                <div className="w-full h-1/2 bg-gradient-to-t from-secondary/10 to-transparent"></div>
              </div>
              <svg className="absolute inset-0 w-full h-full p-4" viewBox="0 0 100 40">
                <path
                  d="M0 35 Q 20 5, 40 30 T 80 15 T 100 35"
                  fill="none"
                  stroke="#ffb2b7"
                  strokeWidth="2"
                  vectorEffect="non-scaling-stroke"
                ></path>
              </svg>
            </div>
          </div>
          <div className="flex justify-between items-center mt-4 pt-4 border-t border-surface-variant">
            <span className="text-xs text-outline">VIX 1D Range</span>
            <span className="text-xs font-bold text-secondary">14.2 - 18.9</span>
          </div>
        </div>
      </section>

      {/* Bento Grid Main Content */}
      <div className="grid grid-cols-12 gap-6">
        {/* Top Signals */}
        <div className="col-span-12 xl:col-span-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="font-headline font-extrabold text-2xl text-on-surface tracking-tight">
              Top Signals
            </h2>
            <div className="flex gap-2">
              <button className="px-3 py-1 bg-surface-container-high text-[10px] font-bold rounded uppercase">
                Filter
              </button>
              <button className="px-3 py-1 bg-surface-container-high text-[10px] font-bold rounded uppercase">
                Export
              </button>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {signals.map((signal) => (
              <div
                key={signal.ticker}
                className="bg-surface-container-low border border-primary/20 p-5 rounded-xl hover:bg-surface-container transition-all group cursor-pointer"
              >
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <span className="text-2xl font-headline font-black text-on-surface group-hover:text-primary transition-colors">
                      {signal.ticker}
                    </span>
                    <p className="text-xs text-outline">{signal.name}</p>
                  </div>
                  <div className="bg-primary/10 text-primary text-[10px] font-bold px-2 py-0.5 rounded border border-primary/20">
                    {signal.signal}
                  </div>
                </div>
                <div className="flex justify-between items-end">
                  <div>
                    <p className="text-2xl font-headline font-bold text-on-surface">{signal.price}</p>
                    <p className={`text-xs flex items-center ${signal.changeColor}`}>
                      <span className="material-symbols-outlined text-sm">
                        {signal.change.startsWith('+') ? 'arrow_drop_up' : 'arrow_drop_down'}
                      </span>
                      {signal.change}
                    </p>
                  </div>
                  <div className="w-24 text-right">
                    <p className="text-[9px] text-outline uppercase mb-1">Sentiment</p>
                    <div className="h-1 bg-surface-container-highest rounded-full overflow-hidden">
                      <div
                        className="h-full bg-primary"
                        style={{ width: `${signal.sentiment}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Technical Heatmap */}
          <div className="mt-8 bg-surface-container-lowest rounded-xl p-6 border border-outline-variant/10">
            <h3 className="font-headline font-bold text-lg mb-6">Technical Heatmap</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
              {[
                { label: 'Tech', change: '+2.4%', color: 'bg-primary/20' },
                { label: 'Energy', change: '+0.8%', color: 'bg-primary/10' },
                { label: 'Finance', change: '-0.4%', color: 'bg-secondary/10' },
                { label: 'Healthcare', change: '-3.2%', color: 'bg-secondary/30' },
                { label: 'Retail', change: '+1.1%', color: 'bg-primary/10' },
                { label: 'Utilities', change: '0.0%', color: 'bg-surface-container' },
                { label: 'Materials', change: '+0.2%', color: 'bg-primary/5' },
                { label: 'Industrial', change: '-1.1%', color: 'bg-secondary/10' },
              ].map((item, i) => (
                <div
                  key={i}
                  className={`${item.color} p-4 rounded border border-primary/10 text-center`}
                >
                  <span className="block text-[10px] text-on-surface-variant font-bold uppercase mb-1">
                    {item.label}
                  </span>
                  <span className="font-headline text-lg text-on-surface font-black">
                    {item.change}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Live Intelligence Feed */}
        <div className="col-span-12 xl:col-span-4">
          <div className="bg-surface-container-low rounded-xl border border-outline-variant/10 h-full flex flex-col">
            <div className="p-6 border-b border-surface-variant/30 flex justify-between items-center">
              <div className="flex items-center gap-3">
                <span className="material-symbols-outlined text-primary">analytics</span>
                <h2 className="font-headline font-bold text-lg">Intelligence Feed</h2>
              </div>
              <span className="w-2 h-2 bg-primary rounded-full animate-pulse"></span>
            </div>
            <div className="flex-1 overflow-y-auto p-4 space-y-4 max-h-[600px]">
              {feedItems.map((item, i) => (
                <div
                  key={i}
                  className="p-4 bg-surface-container rounded-lg border-l-2 border-primary/50 hover:bg-surface-bright transition-colors cursor-pointer group"
                >
                  <div className="flex justify-between items-start mb-2">
                    <span className="text-[9px] font-bold text-outline uppercase tracking-widest">
                      {item.time}
                    </span>
                    <div className="bg-primary-container text-on-primary-container px-1.5 py-0.5 rounded text-[9px] font-bold">
                      {item.sentiment_label}: {item.sentiment.toFixed(2)}
                    </div>
                  </div>
                  <h4 className="text-sm font-semibold text-on-surface leading-snug group-hover:text-primary transition-colors">
                    {item.title}
                  </h4>
                  <div className="mt-3 flex gap-2">
                    {item.tags.map((tag, j) => (
                      <span key={j} className="text-[10px] bg-surface-container-highest px-2 py-0.5 rounded text-on-surface-variant">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
            <div className="p-4 bg-surface-container-lowest text-center">
              <button className="text-xs font-bold text-primary hover:underline">
                View All Intelligence
              </button>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default DashboardPage;
