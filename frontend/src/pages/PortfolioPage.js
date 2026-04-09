import React from 'react';
import Layout from '../components/Layout';

const PortfolioPage = () => {
  const portfolioData = [
    {
      ticker: 'AAPL',
      name: 'Apple Inc.',
      price: '$189.43',
      change: '+1.42%',
      sentiment: 85,
      signal: 'Trending Up',
      signalIcon: 'trending_up',
      recommendation: 'STRONG BUY',
    },
    {
      ticker: 'MSFT',
      name: 'Microsoft Corp.',
      price: '$412.55',
      change: '+0.78%',
      sentiment: 72,
      signal: 'Consolidation',
      signalIcon: 'horizontal_rule',
      recommendation: 'BUY',
    },
    {
      ticker: 'TSLA',
      name: 'Tesla, Inc.',
      price: '$172.63',
      change: '-2.34%',
      sentiment: 31,
      signal: 'RSI Overbought',
      signalIcon: 'trending_down',
      recommendation: 'SELL',
      isNegative: true,
    },
    {
      ticker: 'NVDA',
      name: 'NVIDIA Corporation',
      price: '$890.41',
      change: '+4.51%',
      sentiment: 94,
      signal: 'Volume Breakout',
      signalIcon: 'rocket_launch',
      recommendation: 'STRONG BUY',
    },
  ];

  return (
    <Layout>
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-10">
        <div className="lg:col-span-2 p-8 rounded-xl bg-surface-container-low border border-outline-variant/10 flex items-center justify-between terminal-glow overflow-hidden relative">
          <div className="absolute -right-12 -bottom-12 w-64 h-64 bg-primary/5 rounded-full blur-3xl"></div>
          <div className="relative z-10">
            <span className="text-xs font-bold text-on-surface-variant/60 uppercase tracking-[0.3em] mb-2 block">Executive Summary</span>
            <h2 className="text-4xl font-extrabold font-headline text-on-surface mb-2">
              Portfolio Outlook: <span className="text-primary">Bullish</span>
            </h2>
            <p className="text-on-surface-variant/80 max-w-md text-sm leading-relaxed">Intelligence models confirm high accumulation patterns across 70% of tracked entities.</p>
          </div>
          <div className="flex items-end gap-2 relative z-10">
            <div className="flex flex-col items-center gap-2">
              <div className="w-12 bg-primary rounded-t-sm h-32 buy-signal-glow"></div>
              <span className="text-[10px] font-bold text-primary">4 BUY</span>
            </div>
            <div className="flex flex-col items-center gap-2">
              <div className="w-12 bg-tertiary rounded-t-sm h-16 opacity-60"></div>
              <span className="text-[10px] font-bold text-tertiary">2 HOLD</span>
            </div>
            <div className="flex flex-col items-center gap-2">
              <div className="w-12 bg-secondary rounded-t-sm h-8 sell-signal-glow"></div>
              <span className="text-[10px] font-bold text-secondary">1 SELL</span>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-xl bg-surface-container-high border border-outline-variant/20">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-sm font-bold uppercase tracking-widest text-on-surface">Backtest History</h3>
            <span className="text-[10px] text-on-surface-variant font-medium bg-surface/50 px-2 py-1 rounded">Last 30 Days</span>
          </div>
          <div className="space-y-4">
            <div className="flex justify-between items-end border-b border-outline-variant/10 pb-3">
              <div>
                <p className="text-xs text-on-surface-variant mb-1">Signal Accuracy</p>
                <p className="text-xl font-headline font-bold text-primary">84.2%</p>
              </div>
              <div className="text-right">
                <p className="text-[10px] text-on-surface-variant mb-1">Profitability</p>
                <p className="text-sm font-bold text-on-surface">+12.4%</p>
              </div>
            </div>
            <div className="h-24 w-full bg-surface-container-lowest relative overflow-hidden rounded">
              <div className="absolute inset-0 flex items-end gap-1 px-2 pt-4">
                <div className="flex-1 bg-primary/20 h-[40%] rounded-t-sm"></div>
                <div className="flex-1 bg-primary/30 h-[55%] rounded-t-sm"></div>
                <div className="flex-1 bg-primary/40 h-[45%] rounded-t-sm"></div>
                <div className="flex-1 bg-primary/60 h-[70%] rounded-t-sm"></div>
                <div className="flex-1 bg-primary/80 h-[90%] rounded-t-sm buy-signal-glow"></div>
                <div className="flex-1 bg-primary/50 h-[60%] rounded-t-sm"></div>
                <div className="flex-1 bg-primary/70 h-[80%] rounded-t-sm"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <div className="bg-surface-container-low rounded-xl border border-outline-variant/10 overflow-hidden">
        <div className="px-8 py-6 border-b border-outline-variant/10 flex justify-between items-center">
          <h3 className="text-lg font-headline font-bold text-on-surface">Tracked Tickers</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="text-[10px] uppercase tracking-widest text-on-surface-variant/60 bg-surface-container/30">
                <th className="px-8 py-4 font-bold">Ticker</th>
                <th className="px-6 py-4 font-bold">Price</th>
                <th className="px-6 py-4 font-bold">24h Change</th>
                <th className="px-6 py-4 font-bold text-center">Sentiment</th>
                <th className="px-6 py-4 font-bold">Signal</th>
                <th className="px-8 py-4 font-bold text-right">Recommendation</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-outline-variant/5">
              {portfolioData.map((item) => (
                <tr key={item.ticker} className="hover:bg-surface-variant/20 transition-colors">
                  <td className="px-8 py-6">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded bg-surface-container-highest flex items-center justify-center text-xs font-bold">{item.ticker.substring(0, 2)}</div>
                      <div>
                        <div className="text-sm font-bold">{item.ticker}</div>
                        <div className="text-[10px] text-on-surface-variant">{item.name}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-6 text-sm font-medium">{item.price}</td>
                  <td className="px-6 py-6">
                    <span className={`text-sm font-bold ${item.isNegative ? 'text-secondary' : 'text-primary'}`}>{item.change}</span>
                  </td>
                  <td className="px-6 py-6">
                    <div className="flex flex-col items-center gap-1">
                      <div className="w-24 h-1 bg-surface-container-highest rounded-full overflow-hidden">
                        <div className="h-full bg-primary" style={{ width: `${item.sentiment}%` }}></div>
                      </div>
                      <span className="text-[10px] font-bold text-on-surface-variant">{item.sentiment}</span>
                    </div>
                  </td>
                  <td className="px-6 py-6">
                    <div className="flex items-center gap-2">
                      <span className="material-symbols-outlined text-sm">{item.signalIcon}</span>
                      <span className="text-xs">{item.signal}</span>
                    </div>
                  </td>
                  <td className="px-8 py-6 text-right">
                    <span className={`px-3 py-1 rounded-sm text-[10px] font-bold uppercase ${item.isNegative ? 'bg-secondary/10 text-secondary' : 'bg-primary/10 text-primary'}`}>
                      {item.recommendation}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </Layout>
  );
};

export default PortfolioPage;
