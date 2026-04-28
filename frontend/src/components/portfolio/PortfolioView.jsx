import { useState } from 'react'
import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown, AlertTriangle, Shield, DollarSign, BarChart2 } from 'lucide-react'
import { gtiColor } from '../../data/globe'

const HOLDINGS = [
  { symbol: 'XAUUSD', name: 'Gold',           qty: 2.5,  avgPrice: 2180, currentPrice: 2340, assetClass: 'Commodity', gtiRisk: 85, region: 'Middle East' },
  { symbol: 'SPY',    name: 'S&P 500 ETF',    qty: 40,   avgPrice: 5100, currentPrice: 5204, assetClass: 'Equity',    gtiRisk: 67, region: 'North America' },
  { symbol: 'USOIL',  name: 'Crude Oil WTI',  qty: 10,   avgPrice: 79.0, currentPrice: 82.4, assetClass: 'Commodity', gtiRisk: 80, region: 'Middle East' },
  { symbol: 'USDJPY', name: 'US Dollar/Yen',  qty: 50000, avgPrice: 152.0, currentPrice: 154.22, assetClass: 'Forex', gtiRisk: 70, region: 'Asia Pacific' },
  { symbol: 'GLD',    name: 'Gold ETF',       qty: 30,   avgPrice: 185,  currentPrice: 200,  assetClass: 'Equity',    gtiRisk: 85, region: 'Global' },
  { symbol: 'XOM',    name: 'ExxonMobil',     qty: 60,   avgPrice: 108,  currentPrice: 115,  assetClass: 'Equity',    gtiRisk: 72, region: 'North America' },
  { symbol: 'WHEAT',  name: 'Wheat Futures',  qty: 5,    avgPrice: 540,  currentPrice: 582,  assetClass: 'Commodity', gtiRisk: 88, region: 'Europe' },
  { symbol: 'TLT',    name: 'Treasury Bonds', qty: 100,  avgPrice: 95,   currentPrice: 92,   assetClass: 'Bond',      gtiRisk: 55, region: 'North America' },
]

const CLASS_COLORS = {
  Commodity: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
  Equity:    'text-sky-400 bg-sky-500/10 border-sky-500/20',
  Forex:     'text-purple-400 bg-purple-500/10 border-purple-500/20',
  Bond:      'text-green-400 bg-green-500/10 border-green-500/20',
}

function pnl(h) {
  return (h.currentPrice - h.avgPrice) * h.qty
}
function pnlPct(h) {
  return ((h.currentPrice - h.avgPrice) / h.avgPrice) * 100
}
function totalValue(h) {
  return h.currentPrice * h.qty
}

function StatCard({ icon: Icon, label, value, sub, color = 'text-white' }) {
  return (
    <div className="bg-[#0a0f1e]/80 border border-white/8 rounded-xl p-4">
      <div className="flex items-center gap-2 mb-2">
        <Icon className="h-3.5 w-3.5 text-gray-500" />
        <p className="text-[9px] font-mono uppercase tracking-widest text-gray-500">{label}</p>
      </div>
      <p className={`text-xl font-mono font-bold ${color}`}>{value}</p>
      {sub && <p className="text-[9px] text-gray-500 mt-0.5 font-mono">{sub}</p>}
    </div>
  )
}

function RiskMeter({ value }) {
  const color = value >= 80 ? '#ef4444' : value >= 65 ? '#f59e0b' : '#22c55e'
  const label = value >= 80 ? 'HIGH RISK' : value >= 65 ? 'ELEVATED' : 'MANAGED'
  return (
    <div className="bg-[#0a0f1e]/80 border border-white/8 rounded-xl p-4">
      <div className="flex items-center gap-2 mb-3">
        <Shield className="h-3.5 w-3.5 text-gray-500" />
        <p className="text-[9px] font-mono uppercase tracking-widest text-gray-500">Portfolio GTI Risk</p>
      </div>
      <div className="relative flex items-center justify-center mb-2">
        <svg viewBox="0 0 120 70" className="w-36 h-20">
          <path d="M10 60 A 50 50 0 0 1 110 60" fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth={8} strokeLinecap="round" />
          <path
            d="M10 60 A 50 50 0 0 1 110 60"
            fill="none"
            stroke={color}
            strokeWidth={8}
            strokeLinecap="round"
            strokeDasharray={`${value * 1.57} 157`}
            opacity={0.85}
          />
          <text x="60" y="58" textAnchor="middle" fontSize="18" fontFamily="monospace" fontWeight="bold" fill={color}>{value}</text>
          <text x="60" y="68" textAnchor="middle" fontSize="7" fontFamily="monospace" fill="#6b7280">{label}</text>
        </svg>
      </div>
      <div className="space-y-1">
        {['Geopolitical Exposure', 'Sector Concentration', 'FX Sensitivity'].map((risk, i) => (
          <div key={risk} className="flex items-center justify-between">
            <span className="text-[9px] text-gray-500">{risk}</span>
            <div className="w-20 h-1 bg-white/8 rounded-full overflow-hidden">
              <div className="h-full rounded-full" style={{ width: `${[78, 55, 62][i]}%`, background: color }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default function PortfolioView() {
  const [sort, setSort] = useState('gtiRisk')
  const sorted = [...HOLDINGS].sort((a, b) => {
    if (sort === 'gtiRisk') return b.gtiRisk - a.gtiRisk
    if (sort === 'pnl')     return pnl(b) - pnl(a)
    if (sort === 'value')   return totalValue(b) - totalValue(a)
    return 0
  })

  const totalPnl = HOLDINGS.reduce((s, h) => s + pnl(h), 0)
  const totalVal = HOLDINGS.reduce((s, h) => s + totalValue(h), 0)
  const avgRisk  = Math.round(HOLDINGS.reduce((s, h) => s + h.gtiRisk, 0) / HOLDINGS.length)

  return (
    <div className="flex h-full overflow-hidden">
      {/* Main table */}
      <div className="flex-1 overflow-y-auto p-4">
        {/* Stats row */}
        <div className="grid grid-cols-3 gap-3 mb-4">
          <StatCard
            icon={DollarSign} label="Total Value"
            value={`$${(totalVal / 1000).toFixed(1)}k`}
            color="text-white"
          />
          <StatCard
            icon={BarChart2} label="Total P&L"
            value={`${totalPnl >= 0 ? '+' : ''}$${(totalPnl).toFixed(0)}`}
            color={totalPnl >= 0 ? 'text-green-400' : 'text-red-400'}
            sub={`${totalPnl >= 0 ? '+' : ''}${((totalPnl / (totalVal - totalPnl)) * 100).toFixed(1)}% total return`}
          />
          <StatCard
            icon={AlertTriangle} label="Avg GTI Risk"
            value={String(avgRisk)}
            color={gtiColor(avgRisk)}
            sub="Weighted geopolitical exposure"
          />
        </div>

        {/* Sort controls */}
        <div className="flex items-center gap-2 mb-3">
          <span className="text-[9px] font-mono text-gray-500">Sort:</span>
          {[['gtiRisk', 'GTI Risk'], ['value', 'Value'], ['pnl', 'P&L']].map(([key, label]) => (
            <button key={key} onClick={() => setSort(key)}
              className={`text-[10px] font-mono px-2 py-0.5 rounded border transition-all ${sort === key ? 'bg-sky-500/20 border-sky-500/40 text-sky-300' : 'bg-white/4 border-white/10 text-gray-400 hover:border-white/20'}`}>
              {label}
            </button>
          ))}
        </div>

        {/* Holdings table */}
        <div className="bg-[#0a0f1e]/80 border border-white/8 rounded-xl overflow-hidden">
          <div className="grid grid-cols-[1fr_1fr_1fr_1fr_80px] gap-0 px-4 py-2 border-b border-white/8">
            {['Asset', 'Price / Avg', 'Value', 'P&L', 'GTI Risk'].map(h => (
              <p key={h} className="text-[9px] font-mono uppercase tracking-widest text-gray-500">{h}</p>
            ))}
          </div>
          {sorted.map((h, i) => {
            const p = pnl(h)
            const pp = pnlPct(h)
            const v = totalValue(h)
            const riskColor = gtiColor(h.gtiRisk)
            return (
              <motion.div
                key={h.symbol}
                initial={{ opacity: 0, y: 4 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.04 }}
                className="grid grid-cols-[1fr_1fr_1fr_1fr_80px] gap-0 px-4 py-3 border-b border-white/5 last:border-0 hover:bg-white/3 transition-colors items-center"
              >
                {/* Asset */}
                <div>
                  <div className="flex items-center gap-1.5">
                    <div className="w-1.5 h-1.5 rounded-full" style={{ background: riskColor }} />
                    <span className="text-[12px] font-mono font-semibold text-white">{h.symbol}</span>
                  </div>
                  <div className="flex items-center gap-1 mt-0.5">
                    <span className={`text-[9px] font-mono px-1 py-0.5 rounded border ${CLASS_COLORS[h.assetClass] ?? 'text-gray-400'}`}>
                      {h.assetClass}
                    </span>
                  </div>
                </div>

                {/* Price */}
                <div>
                  <p className="text-[11px] font-mono text-white">{h.currentPrice.toLocaleString()}</p>
                  <p className="text-[9px] font-mono text-gray-500">avg {h.avgPrice.toLocaleString()}</p>
                </div>

                {/* Value */}
                <div>
                  <p className="text-[11px] font-mono text-white">${v.toLocaleString(undefined, { maximumFractionDigits: 0 })}</p>
                  <p className="text-[9px] text-gray-500 font-mono">{h.qty} units</p>
                </div>

                {/* P&L */}
                <div>
                  <div className="flex items-center gap-1">
                    {p >= 0 ? <TrendingUp className="h-3 w-3 text-green-400" /> : <TrendingDown className="h-3 w-3 text-red-400" />}
                    <span className={`text-[11px] font-mono ${p >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                      {p >= 0 ? '+' : ''}${Math.abs(p).toLocaleString(undefined, { maximumFractionDigits: 0 })}
                    </span>
                  </div>
                  <p className={`text-[9px] font-mono ${p >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                    {pp >= 0 ? '+' : ''}{pp.toFixed(1)}%
                  </p>
                </div>

                {/* GTI Risk bar */}
                <div>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-[10px] font-mono" style={{ color: riskColor }}>{h.gtiRisk}</span>
                  </div>
                  <div className="h-1 bg-white/8 rounded-full overflow-hidden">
                    <div className="h-full rounded-full" style={{ width: `${h.gtiRisk}%`, background: riskColor }} />
                  </div>
                  <p className="text-[8px] font-mono text-gray-600 mt-0.5 truncate">{h.region}</p>
                </div>
              </motion.div>
            )
          })}
        </div>
      </div>

      {/* Right panel */}
      <div className="w-72 shrink-0 border-l border-white/8 overflow-y-auto p-4 space-y-3 hidden lg:block">
        <RiskMeter value={avgRisk} />

        {/* Asset class breakdown */}
        <div className="bg-[#0a0f1e]/80 border border-white/8 rounded-xl p-4">
          <p className="text-[9px] font-mono uppercase tracking-widest text-gray-500 mb-3">By Asset Class</p>
          {Object.entries(
            HOLDINGS.reduce((acc, h) => {
              acc[h.assetClass] = (acc[h.assetClass] ?? 0) + totalValue(h)
              return acc
            }, {})
          ).sort((a, b) => b[1] - a[1]).map(([cls, val]) => {
            const pct = Math.round((val / totalVal) * 100)
            return (
              <div key={cls} className="mb-2">
                <div className="flex justify-between mb-0.5">
                  <span className={`text-[10px] font-mono ${CLASS_COLORS[cls]?.split(' ')[0] ?? 'text-gray-400'}`}>{cls}</span>
                  <span className="text-[10px] font-mono text-white">{pct}%</span>
                </div>
                <div className="h-1 bg-white/8 rounded-full overflow-hidden">
                  <div className="h-full rounded-full bg-sky-400/60" style={{ width: `${pct}%` }} />
                </div>
              </div>
            )
          })}
        </div>

        {/* Risk alerts */}
        <div className="bg-[#0a0f1e]/80 border border-white/8 rounded-xl p-4">
          <p className="text-[9px] font-mono uppercase tracking-widest text-gray-500 mb-2">Risk Alerts</p>
          <div className="space-y-2">
            {HOLDINGS.filter(h => h.gtiRisk >= 80).map(h => (
              <div key={h.symbol} className="flex items-start gap-2 py-1.5 border-b border-white/5 last:border-0">
                <AlertTriangle className="h-3 w-3 text-red-400 shrink-0 mt-0.5" />
                <div>
                  <p className="text-[10px] font-mono text-red-300">{h.symbol}</p>
                  <p className="text-[9px] text-gray-500">{h.region} · GTI {h.gtiRisk}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
