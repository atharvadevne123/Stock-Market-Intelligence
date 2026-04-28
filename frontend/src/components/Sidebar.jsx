import { useState } from 'react'
import { X, Play, RotateCcw, AlertTriangle, TrendingUp, TrendingDown, Minus } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { useStore } from '../store'
import { REGION_GTI, gtiColor } from '../data/globe'

const REGIONS = ["North America","Europe","Asia Pacific","Middle East","Latin America","Africa"]
const ASSET_CLASSES = ["Equities","Bonds","Commodities","Forex","Crypto"]
const SCENARIO_KEYS = [
  { key: 'oilShock',    label: 'Oil Price Shock',         color: '#f97316' },
  { key: 'rateChange',  label: 'Interest Rate Change',    color: '#38bdf8' },
  { key: 'escalation',  label: 'Geopolitical Escalation', color: '#ef4444' },
  { key: 'supplyChain', label: 'Supply Chain Disruption', color: '#f59e0b' },
  { key: 'cyberThreat', label: 'Cyber Threat Level',      color: '#a78bfa' },
]

function SimResults({ results, onClear }) {
  const gtiColor_ = results.adjustedGti >= 80 ? '#ef4444' : results.adjustedGti >= 60 ? '#f59e0b' : '#22c55e'
  const gtiLevel  = results.adjustedGti >= 80 ? 'CRITICAL' : results.adjustedGti >= 60 ? 'ELEVATED' : 'NOMINAL'

  return (
    <motion.div
      initial={{ opacity: 0, y: -8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -8 }}
      className="space-y-3"
    >
      {/* Adjusted GTI */}
      <div className="rounded-lg border p-3" style={{ borderColor: gtiColor_ + '40', background: gtiColor_ + '10' }}>
        <div className="flex items-center justify-between mb-1">
          <p className="text-[9px] font-mono uppercase tracking-widest text-gray-500">Simulated GTI</p>
          <button onClick={onClear} className="text-gray-600 hover:text-gray-400 transition-colors">
            <RotateCcw className="h-3 w-3" />
          </button>
        </div>
        <div className="flex items-end gap-2">
          <span className="text-2xl font-mono font-bold" style={{ color: gtiColor_ }}>
            {results.adjustedGti.toFixed(1)}
          </span>
          <span className="text-[9px] font-mono mb-1" style={{ color: gtiColor_ }}>
            {results.gtiDelta >= 0 ? '+' : ''}{results.gtiDelta} vs current
          </span>
          <span className="text-[9px] font-mono mb-1 ml-auto px-1.5 py-0.5 rounded border"
            style={{ color: gtiColor_, borderColor: gtiColor_ + '40', background: gtiColor_ + '15' }}>
            {gtiLevel}
          </span>
        </div>
        <div className="h-1.5 bg-black/30 rounded-full mt-2 overflow-hidden">
          <div className="h-full rounded-full transition-all duration-700"
            style={{ width: `${results.adjustedGti}%`, background: gtiColor_ }} />
        </div>
      </div>

      {/* Asset impacts */}
      <div>
        <p className="text-[9px] font-mono uppercase tracking-widest text-gray-500 mb-2">Asset Impact Forecast</p>
        <div className="space-y-1.5">
          {results.assets.map(({ asset, pct, action }) => {
            const positive = pct >= 0
            const neutral = action === 'HOLD'
            const Icon = neutral ? Minus : positive ? TrendingUp : TrendingDown
            const color = neutral ? '#6b7280' : positive ? '#22c55e' : '#ef4444'
            const actionBg = neutral
              ? 'bg-gray-500/10 border-gray-500/20 text-gray-400'
              : positive
                ? 'bg-green-500/10 border-green-500/25 text-green-400'
                : 'bg-red-500/10 border-red-500/25 text-red-400'
            return (
              <div key={asset} className="flex items-center justify-between py-1 border-b border-white/5 last:border-0">
                <span className="text-[10px] font-mono text-gray-300 w-24 truncate">{asset}</span>
                <div className="flex items-center gap-1.5">
                  <Icon className="h-3 w-3" style={{ color }} />
                  <span className="text-[10px] font-mono" style={{ color }}>
                    {pct >= 0 ? '+' : ''}{pct}%
                  </span>
                  <span className={`text-[8px] font-mono px-1 py-0.5 rounded border ${actionBg}`}>
                    {action}
                  </span>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Alerts */}
      {results.alerts.length > 0 && (
        <div>
          <p className="text-[9px] font-mono uppercase tracking-widest text-gray-500 mb-2">Scenario Alerts</p>
          <div className="space-y-1.5">
            {results.alerts.map((alert, i) => (
              <div key={i} className="flex gap-2 py-1.5 px-2 rounded-lg bg-amber-500/8 border border-amber-500/20">
                <AlertTriangle className="h-3 w-3 text-amber-400 shrink-0 mt-0.5" />
                <p className="text-[9px] text-amber-200 leading-snug">{alert}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  )
}

export default function Sidebar({ open, onClose }) {
  const { selectedRegions, toggleRegion, scenario, updateScenario, simResults, runSimulation, clearSimResults } = useStore()
  const [running, setRunning] = useState(false)

  const handleRun = () => {
    setRunning(true)
    clearSimResults()
    setTimeout(() => {
      runSimulation()
      setRunning(false)
    }, 800)
  }

  return (
    <>
      {open && <div className="fixed inset-0 bg-black/40 z-30 md:hidden" onClick={onClose} />}

      <aside className={`
        w-72 shrink-0 bg-[#0a0f1e]/95 backdrop-blur-xl border-r border-white/8
        flex flex-col overflow-y-auto
        transition-all duration-200
        md:translate-x-0 md:relative md:flex
        ${open ? 'translate-x-0 fixed left-0 top-0 h-full z-40' : '-translate-x-full fixed left-0 top-0 h-full z-40 md:translate-x-0 hidden md:block'}
      `}>
        <div className="flex items-center justify-between px-4 py-3 border-b border-white/8">
          <span className="text-[10px] font-mono uppercase tracking-widest text-gray-400">Intelligence Controls</span>
          <button onClick={onClose} className="md:hidden text-gray-400 hover:text-white">
            <X className="h-4 w-4" />
          </button>
        </div>

        <div className="flex-1 p-4 space-y-6">
          {/* GTI Region Breakdown */}
          <section>
            <h3 className="text-[9px] font-mono uppercase tracking-widest text-gray-500 mb-3">GTI Region Breakdown</h3>
            <div className="space-y-2">
              {REGION_GTI.map(({ region, score, driver, weight, delta }) => (
                <div key={region}>
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-[11px] text-gray-300">{region}</span>
                    <div className="flex items-center gap-1.5">
                      <span className={`text-[10px] font-mono ${score >= 80 ? 'text-red-400' : score >= 60 ? 'text-amber-400' : 'text-green-400'}`}>{score}</span>
                      <span className={`text-[9px] font-mono ${delta >= 0 ? 'text-red-400' : 'text-green-400'}`}>{delta >= 0 ? `+${delta.toFixed(1)}` : delta.toFixed(1)}</span>
                    </div>
                  </div>
                  <div className="h-1 bg-white/6 rounded-full overflow-hidden">
                    <div className="h-full rounded-full transition-all duration-700"
                      style={{ width: `${score}%`, background: score >= 80 ? '#ef4444' : score >= 60 ? '#f59e0b' : '#22c55e' }} />
                  </div>
                  <p className="text-[9px] text-gray-600 mt-0.5">{driver} · {Math.round(weight * 100)}%</p>
                </div>
              ))}
            </div>
          </section>

          {/* Region Filter */}
          <section>
            <h3 className="text-[9px] font-mono uppercase tracking-widest text-gray-500 mb-3">Filter by Region</h3>
            <div className="flex flex-wrap gap-1.5">
              {REGIONS.map(r => {
                const active = selectedRegions.includes(r)
                return (
                  <button key={r} onClick={() => toggleRegion(r)}
                    className={`text-[10px] px-2 py-1 rounded border font-mono transition-all
                      ${active ? 'bg-sky-500/20 border-sky-500/50 text-sky-300' : 'bg-white/4 border-white/12 text-gray-400 hover:border-white/20'}`}>
                    {r}
                  </button>
                )
              })}
            </div>
          </section>

          {/* Asset Classes */}
          <section>
            <h3 className="text-[9px] font-mono uppercase tracking-widest text-gray-500 mb-3">Asset Classes</h3>
            <div className="flex flex-wrap gap-1.5">
              {ASSET_CLASSES.map(a => (
                <button key={a}
                  className="text-[10px] px-2 py-1 rounded border bg-white/4 border-white/12 text-gray-400 hover:border-white/20 font-mono transition-all">
                  {a}
                </button>
              ))}
            </div>
          </section>

          {/* Scenario Simulator */}
          <section>
            <h3 className="text-[9px] font-mono uppercase tracking-widest text-gray-500 mb-3">Scenario Simulator</h3>
            <div className="space-y-3">
              {SCENARIO_KEYS.map(({ key, label, color }) => (
                <div key={key}>
                  <div className="flex justify-between mb-1">
                    <span className="text-[10px] text-gray-400">{label}</span>
                    <span className="text-[10px] font-mono text-white">{scenario[key]}</span>
                  </div>
                  <div className="relative">
                    <input
                      type="range" min={0} max={100} value={scenario[key]}
                      onChange={e => { updateScenario(key, +e.target.value); clearSimResults() }}
                      className="w-full h-1 appearance-none bg-white/10 rounded-full cursor-pointer"
                      style={{ accentColor: color }}
                    />
                    <div className="h-1 rounded-full pointer-events-none absolute top-0 left-0"
                      style={{ width: `${scenario[key]}%`, background: color, opacity: 0.5 }} />
                  </div>
                </div>
              ))}

              <button
                onClick={handleRun}
                disabled={running}
                className={`w-full mt-2 py-2 text-[11px] font-mono font-semibold rounded tracking-wider uppercase flex items-center justify-center gap-2 transition-all
                  ${running
                    ? 'border border-sky-500/20 text-sky-600 cursor-not-allowed'
                    : 'border border-sky-500/40 text-sky-400 hover:bg-sky-500/10 hover:border-sky-500/60'
                  }`}
              >
                {running ? (
                  <>
                    <svg className="animate-spin h-3 w-3" viewBox="0 0 24 24" fill="none">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
                    </svg>
                    Running...
                  </>
                ) : (
                  <>
                    <Play className="h-3 w-3" />
                    Run Simulation
                  </>
                )}
              </button>
            </div>
          </section>

          {/* Simulation Results */}
          <AnimatePresence>
            {simResults && (
              <section>
                <h3 className="text-[9px] font-mono uppercase tracking-widest text-gray-500 mb-3">Simulation Output</h3>
                <SimResults results={simResults} onClear={clearSimResults} />
              </section>
            )}
          </AnimatePresence>
        </div>
      </aside>
    </>
  )
}
