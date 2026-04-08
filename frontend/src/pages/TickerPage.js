import React from 'react';
import Layout from '../components/Layout';

const TickerPage = () => {
  return (
    <Layout>
      {/* Hero Section: NVDA Identity */}
      <div className="flex justify-between items-end mb-10">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <div className="w-12 h-12 rounded-lg bg-primary-container flex items-center justify-center border border-primary/20">
              <span className="material-symbols-outlined text-primary text-3xl">memory</span>
            </div>
            <div>
              <h1 className="text-4xl font-extrabold font-headline tracking-tighter text-on-surface uppercase">
                NVDA
              </h1>
              <p className="text-on-surface-variant text-sm font-medium tracking-wide">
                NVIDIA Corporation • NASDAQ
              </p>
            </div>
          </div>
          <div className="flex gap-4 mt-4">
            <div className="bg-surface-container-low px-3 py-1 rounded-full border border-outline-variant/10 text-[10px] font-bold text-on-surface-variant uppercase tracking-widest">
              Semiconductors
            </div>
            <div className="bg-surface-container-low px-3 py-1 rounded-full border border-outline-variant/10 text-[10px] font-bold text-on-surface-variant uppercase tracking-widest">
              AI & Data Center
            </div>
          </div>
        </div>
        <div className="text-right">
          <div className="text-5xl font-extrabold font-headline tracking-tight mb-1">
            $894.22
          </div>
          <div className="flex items-center justify-end gap-2 text-primary font-bold">
            <span className="material-symbols-outlined text-sm">arrow_upward</span>
            <span>+24.18 (2.78%)</span>
          </div>
        </div>
      </div>

      {/* Main Bento Grid */}
      <div className="grid grid-cols-12 gap-6">
        {/* Section 1: Signal Summary */}
        <div className="col-span-12 lg:col-span-4 bg-surface-container-low rounded-xl p-6 relative overflow-hidden flex flex-col justify-between group">
          <div className="absolute top-0 right-0 p-4 opacity-10">
            <span className="material-symbols-outlined text-9xl text-primary">shield_with_heart</span>
          </div>
          <div>
            <div className="text-[10px] font-bold text-primary uppercase tracking-[0.2em] mb-4">
              Master Signal Indicator
            </div>
            <div className="text-6xl font-extrabold font-headline text-primary leading-none mb-2 tracking-tighter">
              STRONG BUY
            </div>
            <div className="flex items-center gap-2 mb-6">
              <div className="h-1 w-full bg-surface-container-highest rounded-full overflow-hidden">
                <div className="h-full bg-primary w-[92%] shadow-[0_0_10px_rgba(78,222,163,0.5)]"></div>
              </div>
              <span className="text-xl font-bold font-headline text-on-surface">92%</span>
            </div>
          </div>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-[10px] font-bold uppercase tracking-widest text-on-surface-variant mb-1">
                <span>Technical Weight</span>
                <span>70%</span>
              </div>
              <div className="h-1 bg-surface-container-highest rounded-full overflow-hidden">
                <div className="h-full bg-primary-fixed-dim w-[70%]"></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-[10px] font-bold uppercase tracking-widest text-on-surface-variant mb-1">
                <span>Sentiment Weight</span>
                <span>30%</span>
              </div>
              <div className="h-1 bg-surface-container-highest rounded-full overflow-hidden">
                <div className="h-full bg-tertiary w-[30%]"></div>
              </div>
            </div>
          </div>
        </div>

        {/* Section 2: Technical Chart & Indicators */}
        <div className="col-span-12 lg:col-span-8 bg-surface-container-low rounded-xl flex overflow-hidden">
          <div className="flex-1 p-6 relative bg-surface-container-lowest">
            <div className="flex justify-between items-center mb-6">
              <div className="flex gap-2">
                <button className="px-2 py-1 bg-surface-container-high rounded text-[10px] font-bold">
                  1H
                </button>
                <button className="px-2 py-1 bg-primary text-on-primary rounded text-[10px] font-bold">
                  4H
                </button>
                <button className="px-2 py-1 bg-surface-container-high rounded text-[10px] font-bold">
                  1D
                </button>
                <button className="px-2 py-1 bg-surface-container-high rounded text-[10px] font-bold">
                  1W
                </button>
              </div>
              <div className="text-[10px] font-bold text-outline-variant uppercase tracking-widest">
                Real-Time Data Execution
              </div>
            </div>
            <div className="h-[280px] w-full relative">
              <div className="absolute inset-0 bg-gradient-to-t from-primary/5 to-transparent"></div>
              <svg className="w-full h-full" preserveAspectRatio="none" viewBox="0 0 100 100">
                <path
                  d="M0,80 L10,75 L20,78 L30,65 L40,68 L50,45 L60,50 L70,30 L80,35 L90,15 L100,20"
                  fill="none"
                  stroke="#4edea3"
                  strokeWidth="1.5"
                ></path>
                <line stroke="#2d3449" strokeDasharray="2" x1="0" x2="100" y1="50" y2="50"></line>
              </svg>
              <div className="absolute bottom-10 left-1/2 w-4 h-4 bg-primary rounded-full blur-md animate-pulse"></div>
            </div>
          </div>
          <div className="w-64 border-l border-outline-variant/10 p-6 flex flex-col gap-6">
            <div className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest">
              Oscillators
            </div>
            <div className="space-y-4">
              <div className="bg-surface-container-lowest p-3 rounded border border-outline-variant/5">
                <div className="flex justify-between text-[10px] mb-1">
                  <span className="text-on-surface-variant">RSI (14)</span>
                  <span className="text-primary font-bold">32.4</span>
                </div>
                <div className="text-xs font-bold text-primary uppercase">Oversold</div>
              </div>
              <div className="bg-surface-container-lowest p-3 rounded border border-outline-variant/5">
                <div className="flex justify-between text-[10px] mb-1">
                  <span className="text-on-surface-variant">MACD</span>
                  <span className="text-primary font-bold">14.2</span>
                </div>
                <div className="text-xs font-bold text-primary uppercase">Bullish Crossover</div>
              </div>
              <div className="bg-surface-container-lowest p-3 rounded border border-outline-variant/5">
                <div className="flex justify-between text-[10px] mb-1">
                  <span className="text-on-surface-variant">BOLLINGER</span>
                  <span className="text-tertiary font-bold">LOWER</span>
                </div>
                <div className="text-xs font-bold text-tertiary uppercase">Price at Band</div>
              </div>
            </div>
          </div>
        </div>

        {/* Section 3: Sentiment Analysis */}
        <div className="col-span-12 lg:col-span-8 bg-surface-container-low rounded-xl p-8">
          <div className="flex justify-between items-center mb-8">
            <h3 className="font-headline text-xl font-bold uppercase tracking-tight">
              FinBERT Neural Sentiment
            </h3>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <div className="text-[10px] text-on-surface-variant uppercase font-bold tracking-widest">
                  Aggregate Score
                </div>
                <div className="text-2xl font-extrabold text-primary font-headline tracking-tighter">
                  0.92 POSITIVE
                </div>
              </div>
              <div className="w-12 h-12 rounded-full border-4 border-surface-container-highest flex items-center justify-center relative">
                <svg className="w-full h-full -rotate-90">
                  <circle cx="24" cy="24" fill="none" r="20" stroke="#4edea3" strokeDasharray="125.6" strokeDashoffset="10" strokeWidth="4"></circle>
                </svg>
                <span className="absolute text-[10px] font-bold">92</span>
              </div>
            </div>
          </div>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-surface-container-lowest rounded-lg border-l-4 border-primary/40 group hover:bg-surface-container-high transition-colors">
              <div className="flex gap-4 items-center">
                <div className="w-10 h-10 rounded bg-surface-container-highest flex items-center justify-center text-primary">
                  <span className="material-symbols-outlined">newspaper</span>
                </div>
                <div>
                  <div className="text-sm font-bold text-on-surface">
                    Blackwell Chip Production Scaling Ahead of Schedule
                  </div>
                  <div className="text-[10px] text-on-surface-variant font-medium">
                    Source: Bloomberg Intelligence • 2h ago
                  </div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-xs font-bold text-primary">+0.94</div>
                <div className="text-[9px] text-outline-variant uppercase">Positive</div>
              </div>
            </div>
            <div className="flex items-center justify-between p-4 bg-surface-container-lowest rounded-lg border-l-4 border-primary/20 group hover:bg-surface-container-high transition-colors">
              <div className="flex gap-4 items-center">
                <div className="w-10 h-10 rounded bg-surface-container-highest flex items-center justify-center text-secondary">
                  <span className="material-symbols-outlined">forum</span>
                </div>
                <div>
                  <div className="text-sm font-bold text-on-surface">
                    "NVDA dip is the ultimate generational buying opportunity"
                  </div>
                  <div className="text-[10px] text-on-surface-variant font-medium">
                    r/WallStreetBets • 5h ago
                  </div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-xs font-bold text-primary">+0.81</div>
                <div className="text-[9px] text-outline-variant uppercase">Positive</div>
              </div>
            </div>
            <div className="flex items-center justify-between p-4 bg-surface-container-lowest rounded-lg border-l-4 border-tertiary/40 group hover:bg-surface-container-high transition-colors">
              <div className="flex gap-4 items-center">
                <div className="w-10 h-10 rounded bg-surface-container-highest flex items-center justify-center text-tertiary">
                  <span className="material-symbols-outlined">lab_profile</span>
                </div>
                <div>
                  <div className="text-sm font-bold text-on-surface">
                    Regulatory Concerns in EU Market Regarding GPU Monopoly
                  </div>
                  <div className="text-[10px] text-on-surface-variant font-medium">
                    Source: Reuters • 8h ago
                  </div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-xs font-bold text-tertiary">-0.12</div>
                <div className="text-[9px] text-outline-variant uppercase">Neutral</div>
              </div>
            </div>
          </div>
        </div>

        {/* Section 4: Earnings Insight */}
        <div className="col-span-12 lg:col-span-4 bg-surface-container-low rounded-xl p-8 relative">
          <div className="mb-6">
            <div className="text-[10px] font-bold text-tertiary uppercase tracking-widest mb-2">
              Earnings Intelligence
            </div>
            <h3 className="font-headline text-xl font-bold uppercase tracking-tight">
              Q3 CEO Discourse
            </h3>
          </div>
          <div className="p-4 bg-surface-container-lowest rounded border border-outline-variant/10 italic text-on-surface-variant text-sm leading-relaxed mb-6">
            "The next industrial revolution has begun. We are seeing unprecedented demand for
            Blackwell as sovereign nations build their AI factories..."
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-surface-container-high p-4 rounded text-center">
              <div className="text-[10px] font-bold text-outline-variant uppercase mb-1">
                CEO Confidence
              </div>
              <div className="text-2xl font-extrabold text-primary font-headline">9.8/10</div>
            </div>
            <div className="bg-surface-container-high p-4 rounded text-center">
              <div className="text-[10px] font-bold text-outline-variant uppercase mb-1">
                Key Phrase
              </div>
              <div className="text-xs font-extrabold text-on-surface uppercase leading-tight mt-1">
                Sovereign AI
              </div>
            </div>
          </div>
          <div className="mt-8">
            <div className="flex justify-between text-[10px] font-bold uppercase mb-2">
              <span className="text-on-surface-variant">AI Hype Index</span>
              <span className="text-primary">Extreme</span>
            </div>
            <div className="h-2 bg-surface-container-highest rounded-full overflow-hidden flex">
              <div className="h-full bg-primary/20 w-1/3 border-r border-surface"></div>
              <div className="h-full bg-primary/40 w-1/3 border-r border-surface"></div>
              <div className="h-full bg-primary w-1/3 shadow-[0_0_15px_rgba(78,222,163,0.3)]"></div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Action Bar */}
      <div className="fixed bottom-8 right-8 flex gap-4 z-40">
        <button className="px-8 py-3 bg-secondary-container text-on-secondary-container rounded-lg font-bold uppercase tracking-widest text-xs flex items-center gap-2 shadow-lg hover:brightness-110 transition-all active:scale-95">
          <span className="material-symbols-outlined text-sm">trending_down</span>
          Short Position
        </button>
        <button className="px-12 py-3 bg-gradient-to-br from-primary to-on-primary-container text-on-primary rounded-lg font-bold uppercase tracking-widest text-xs flex items-center gap-2 shadow-lg hover:brightness-110 transition-all active:scale-95">
          <span className="material-symbols-outlined text-sm">trending_up</span>
          Open Long Trade
        </button>
      </div>
    </Layout>
  );
};

export default TickerPage;
