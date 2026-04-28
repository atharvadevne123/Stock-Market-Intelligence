import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { TrendingUp, TrendingDown, Minus, ChevronDown, ChevronUp, Activity, Zap, Brain } from 'lucide-react'
import { AreaChart, Area, ResponsiveContainer, XAxis, YAxis, Tooltip } from 'recharts'
import { SIGNALS, NLP_STATS, GTI_HISTORY } from '../../data/signals'
import { useStore } from '../../store'

const ACTION_STYLES = {
  BUY:  { text: 'text-green-400',  bg: 'bg-green-500/10  border-green-500/30',  dot: 'bg-green-400'  },
  SELL: { text: 'text-red-400',    bg: 'bg-red-500/10    border-red-500/30',    dot: 'bg-red-400'    },
  HOLD: { text: 'text-amber-400',  bg: 'bg-amber-500/10  border-amber-500/30',  dot: 'bg-amber-400'  },
}

const CLASS_LABELS = {
  commodity: 'CMDTY',
  equity:    'EQ',
  currency:  'FX',
}

function ConfBar({ value, color = '#22c55e' }) {
  return (
    <div className="h-1 bg-white/8 rounded-full overflow-hidden">
      <motion.div
        initial={{ width: 0 }}
        animate={{ width: `${value}%` }}
        transition={{ duration: 0.8, ease: 'easeOut' }}
        className="h-full rounded-full"
        style={{ background: color }}
      />
    </div>
  )
}

function SignalCard({ signal }) {
  const { expandedSignal, setExpandedSignal } = useStore()
  const expanded = expandedSignal === signal.asset
  const S = ACTION_STYLES[signal.action]
  const confColor = signal.confidence >= 80 ? '#22c55e' : signal.confidence >= 65 ? '#f59e0b' : '#ef4444'

  return (
    <motion.div
      layout
      className="bg-[#0a0f1e]/80 border border-white/8 rounded-xl overflow-hidden hover:border-white/15 transition-colors"
    >
      {/* Header */}
      <div
        className="px-4 py-3 cursor-pointer select-none"
        onClick={() => setExpandedSignal(signal.asset)}
      >
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-2 mb-1">
              <span className={`text-[9px] font-mono px-1.5 py-0.5 rounded border ${S.bg} ${S.text}`}>
                {signal.action}
              </span>
              <span className="text-[9px] font-mono text-gray-600 px-1.5 py-0.5 rounded bg-white/5 border border-white/8">
                {CLASS_LABELS[signal.assetClass] ?? signal.assetClass.toUpperCase()}
              </span>
            </div>
            <p className="text-[13px] font-mono font-semibold text-white truncate">{signal.asset}</p>
            <p className="text-[10px] text-gray-500 mt-0.5 leading-relaxed line-clamp-2">{signal.summary}</p>
          </div>

          <div className="flex flex-col items-end shrink-0 gap-1">
            <div className="flex items-center gap-1">
              <span className="text-[11px] font-mono text-white">{signal.price}</span>
              {signal.changeDir > 0
                ? <TrendingUp className="h-3 w-3 text-green-400" />
                : signal.changeDir < 0
                  ? <TrendingDown className="h-3 w-3 text-red-400" />
                  : <Minus className="h-3 w-3 text-gray-500" />
              }
              <span className={`text-[10px] font-mono ${signal.changeDir > 0 ? 'text-green-400' : signal.changeDir < 0 ? 'text-red-400' : 'text-gray-500'}`}>
                {signal.change}
              </span>
            </div>

            {/* Confidence gauge */}
            <div className="text-right">
              <span className="text-[9px] font-mono text-gray-500">CONF </span>
              <span className="text-[13px] font-mono font-bold" style={{ color: confColor }}>{signal.confidence}%</span>
            </div>
            <div className="w-24">
              <ConfBar value={signal.confidence} color={confColor} />
            </div>
          </div>
        </div>

        {/* Trigger tag */}
        <div className="mt-2 flex items-center justify-between">
          <div className="flex items-center gap-1.5">
            <Zap className="h-3 w-3 text-amber-400 shrink-0" />
            <span className="text-[10px] font-mono text-amber-400 truncate">{signal.trigger}</span>
          </div>
          {expanded ? <ChevronUp className="h-3.5 w-3.5 text-gray-600" /> : <ChevronDown className="h-3.5 w-3.5 text-gray-600" />}
        </div>
      </div>

      {/* Expanded chain */}
      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25 }}
            className="overflow-hidden"
          >
            <div className="px-4 pb-4 border-t border-white/6 pt-3 space-y-3">
              {/* Impact path */}
              <div>
                <p className="text-[9px] font-mono uppercase tracking-widest text-gray-500 mb-2">Impact Chain</p>
                <div className="flex items-center gap-1.5 flex-wrap">
                  {signal.path.map((node, i) => (
                    <div key={i} className="flex items-center gap-1.5">
                      <span className="text-[10px] font-mono text-sky-300 bg-sky-500/10 border border-sky-500/20 px-2 py-0.5 rounded">
                        {node}
                      </span>
                      {i < signal.path.length - 1 && <span className="text-gray-600 text-[10px]">→</span>}
                    </div>
                  ))}
                </div>
              </div>

              {/* Reasoning steps */}
              <div>
                <p className="text-[9px] font-mono uppercase tracking-widest text-gray-500 mb-2">AI Reasoning</p>
                <div className="space-y-2">
                  {signal.chain.map((step) => (
                    <div key={step.step} className="flex gap-2.5">
                      <span className="text-[9px] font-mono text-sky-400 bg-sky-500/10 border border-sky-500/20 rounded w-4 h-4 flex items-center justify-center shrink-0 mt-0.5">
                        {step.step}
                      </span>
                      <div className="flex-1 min-w-0">
                        <p className="text-[11px] text-white leading-snug">{step.desc}</p>
                        <p className="text-[9px] text-gray-500 mt-0.5">{step.evidence}</p>
                        <div className="flex items-center gap-1.5 mt-1">
                          <div className="flex-1 h-0.5 bg-white/8 rounded-full overflow-hidden">
                            <div className="h-full bg-sky-400/60 rounded-full" style={{ width: `${step.conf * 100}%` }} />
                          </div>
                          <span className="text-[9px] font-mono text-gray-500">{(step.conf * 100).toFixed(0)}%</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Uncertainty */}
              <div className="flex items-center gap-2 pt-1">
                <span className="text-[9px] font-mono text-gray-500">Uncertainty:</span>
                <div className="flex-1 h-1 bg-white/8 rounded-full overflow-hidden">
                  <div className="h-full bg-red-400/50 rounded-full" style={{ width: `${signal.uncertainty}%` }} />
                </div>
                <span className="text-[9px] font-mono text-red-400">{signal.uncertainty}%</span>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}

function NlpPanel() {
  return (
    <div className="bg-[#0a0f1e]/80 border border-white/8 rounded-xl p-4 space-y-3">
      <div className="flex items-center gap-2 mb-1">
        <Brain className="h-3.5 w-3.5 text-purple-400" />
        <p className="text-[9px] font-mono uppercase tracking-widest text-gray-400">NLP Intelligence Engine</p>
      </div>
      <div className="grid grid-cols-2 gap-2">
        <div className="bg-white/4 rounded-lg p-2.5">
          <p className="text-[9px] font-mono text-gray-500 mb-0.5">Articles Processed</p>
          <p className="text-lg font-mono font-bold text-white">{NLP_STATS.articles_processed.toLocaleString()}</p>
        </div>
        <div className="bg-white/4 rounded-lg p-2.5">
          <p className="text-[9px] font-mono text-gray-500 mb-0.5">Sentiment Score</p>
          <p className={`text-lg font-mono font-bold ${NLP_STATS.sentiment_score < 0 ? 'text-red-400' : 'text-green-400'}`}>
            {NLP_STATS.sentiment_score.toFixed(2)}
          </p>
        </div>
        <div className="bg-white/4 rounded-lg p-2.5">
          <p className="text-[9px] font-mono text-gray-500 mb-0.5">Macro Narratives</p>
          <p className="text-lg font-mono font-bold text-white">{NLP_STATS.macro_narratives}</p>
        </div>
        <div className="bg-white/4 rounded-lg p-2.5">
          <p className="text-[9px] font-mono text-gray-500 mb-0.5">Model</p>
          <p className="text-[11px] font-mono font-bold text-sky-400">LightGBM</p>
        </div>
      </div>
      <div>
        <p className="text-[9px] font-mono text-gray-500 mb-1.5">Top Detected Topics</p>
        <div className="flex flex-wrap gap-1">
          {NLP_STATS.top_topics.map(t => (
            <span key={t} className="text-[9px] font-mono px-2 py-0.5 rounded bg-purple-500/10 border border-purple-500/20 text-purple-300">{t}</span>
          ))}
        </div>
      </div>
    </div>
  )
}

function GtiChart() {
  return (
    <div className="bg-[#0a0f1e]/80 border border-white/8 rounded-xl p-4">
      <div className="flex items-center gap-2 mb-3">
        <Activity className="h-3.5 w-3.5 text-sky-400" />
        <p className="text-[9px] font-mono uppercase tracking-widest text-gray-400">GTI — 48h History</p>
      </div>
      <ResponsiveContainer width="100%" height={80}>
        <AreaChart data={GTI_HISTORY} margin={{ top: 2, right: 2, left: -30, bottom: 0 }}>
          <defs>
            <linearGradient id="gtiGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%"  stopColor="#0ea5e9" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0} />
            </linearGradient>
          </defs>
          <XAxis dataKey="hour" tick={false} axisLine={false} tickLine={false} />
          <YAxis domain={[55, 80]} tick={{ fontSize: 8, fill: '#6b7280', fontFamily: 'monospace' }} axisLine={false} tickLine={false} />
          <Tooltip
            contentStyle={{ background: '#0a0f1e', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 6, fontSize: 10, fontFamily: 'monospace' }}
            labelFormatter={v => `${v}h ago`}
            formatter={v => [v.toFixed(1), 'GTI']}
          />
          <Area type="monotone" dataKey="value" stroke="#0ea5e9" strokeWidth={1.5} fill="url(#gtiGrad)" dot={false} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}

export default function SignalsView() {
  return (
    <div className="flex h-full overflow-hidden">
      {/* Signal cards */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        <div className="flex items-center justify-between mb-1">
          <div>
            <h2 className="text-[11px] font-mono font-bold text-white uppercase tracking-widest">AI Trading Signals</h2>
            <p className="text-[9px] font-mono text-gray-500 mt-0.5">Geopolitical event → market impact chain</p>
          </div>
          <span className="text-[9px] font-mono text-sky-400 px-2 py-1 bg-sky-500/10 border border-sky-500/20 rounded">
            {SIGNALS.length} ACTIVE
          </span>
        </div>
        {SIGNALS.map(sig => <SignalCard key={sig.asset} signal={sig} />)}
      </div>

      {/* Right panel */}
      <div className="w-72 shrink-0 border-l border-white/8 overflow-y-auto p-4 space-y-3 hidden lg:block">
        <GtiChart />
        <NlpPanel />
        {/* Model info */}
        <div className="bg-[#0a0f1e]/80 border border-white/8 rounded-xl p-4 space-y-2">
          <p className="text-[9px] font-mono uppercase tracking-widest text-gray-500">Pipeline</p>
          {[
            ['Event Classifier', 'Transformer'],
            ['Sentiment Model', 'FinBERT'],
            ['Price Model', 'LightGBM'],
            ['Update Cycle', '15 min'],
            ['Data Sources', 'GDELT · Reuters · UN'],
          ].map(([label, val]) => (
            <div key={label} className="flex justify-between items-center">
              <span className="text-[10px] text-gray-500">{label}</span>
              <span className="text-[10px] font-mono text-white">{val}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
