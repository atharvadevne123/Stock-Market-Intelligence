import { useEffect, useState } from 'react'
import { Activity, Globe, Map, BarChart2, Briefcase, Menu, X, TrendingUp, TrendingDown, Minus, Zap } from 'lucide-react'
import { useStore } from '../store'
import { GTI_VALUE, GTI_DELTA_1H } from '../data/globe'

const TABS = [
  { id: 'globe',     label: 'EARTH PULSE', sub: 'Global Intelligence Globe',   Icon: Globe },
  { id: 'map',       label: 'GEO MAP',     sub: 'Market Impact Map',           Icon: Map },
  { id: 'charts',    label: 'AI SIGNALS',  sub: 'Trading Recommendations',     Icon: BarChart2 },
  { id: 'portfolio', label: 'PORTFOLIO',   sub: 'My Holdings & Risk',          Icon: Briefcase },
]

function LiveClock() {
  const [time, setTime] = useState(() => new Date().toISOString().substring(11, 19))
  useEffect(() => {
    const t = setInterval(() => setTime(new Date().toISOString().substring(11, 19)), 1000)
    return () => clearInterval(t)
  }, [])
  return <span className="font-mono text-[11px] tabular-nums text-gray-400">{time} UTC</span>
}

function GtiStatus({ value, delta }) {
  const status = value >= 80 ? 'CRITICAL' : value >= 60 ? 'ELEVATED' : 'NOMINAL'
  const textColor = value >= 80 ? 'text-red-400' : value >= 60 ? 'text-amber-400' : 'text-green-400'
  const bgColor = value >= 80 ? 'bg-red-500/10 border-red-500/20' : value >= 60 ? 'bg-amber-500/10 border-amber-500/20' : 'bg-green-500/10 border-green-500/20'
  const DeltaIcon = delta > 0 ? TrendingUp : delta < 0 ? TrendingDown : Minus
  const deltaColor = delta > 0 ? 'text-red-400' : delta < 0 ? 'text-green-400' : 'text-gray-500'

  return (
    <div className="hidden sm:flex items-center gap-3">
      <Activity className="h-4 w-4 text-gray-500 shrink-0" />
      <div>
        <p className="text-[9px] font-mono uppercase tracking-widest text-gray-500 leading-none mb-1">
          Global Tension Index
        </p>
        <div className="flex items-center gap-2">
          <span className={`text-xl font-mono font-bold tabular-nums leading-none ${textColor}`}>
            {value.toFixed(1)}
          </span>
          <div className="flex items-center gap-1">
            <DeltaIcon className={`h-3 w-3 ${deltaColor}`} />
            <span className={`text-[10px] font-mono ${deltaColor}`}>
              {delta > 0 ? '+' : ''}{delta.toFixed(1)}
            </span>
          </div>
          <span className={`text-[9px] font-mono px-1.5 py-0.5 rounded border ${bgColor} ${textColor}`}>
            {status}
          </span>
        </div>
      </div>
    </div>
  )
}

export default function Header({ onMenuToggle, menuOpen }) {
  const { mode, setMode } = useStore()

  return (
    <header className="w-full bg-[#07091a]/95 backdrop-blur-xl border-b border-white/10 shadow-lg shrink-0 z-50">
      {/* Top bar */}
      <div className="flex items-center justify-between px-3 sm:px-5 py-2 sm:py-2.5 min-h-[52px]">
        {/* Left: hamburger + logo */}
        <div className="flex items-center gap-2 sm:gap-5 min-w-0">
          <button onClick={onMenuToggle} aria-label={menuOpen ? 'Close menu' : 'Open menu'}
            className="md:hidden flex items-center justify-center w-9 h-9 rounded-lg border border-white/15 bg-white/3 text-white hover:bg-white/5 transition-colors shrink-0">
            {menuOpen ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
          </button>

          {/* Logo */}
          <div className="flex items-center gap-2 shrink-0">
            <div className="h-8 w-8 rounded-lg bg-white/5 border border-white/15 flex items-center justify-center">
              <Zap className="h-4 w-4 text-sky-400" />
            </div>
            <div>
              <p className="text-[13px] font-bold font-mono tracking-[0.18em] text-white leading-none">SOVEREIGN</p>
              <p className="text-[8px] font-mono text-white/50 tracking-widest leading-none mt-0.5">TERMINAL v2.0</p>
            </div>
          </div>

          <div className="hidden sm:block w-px h-8 bg-white/8 shrink-0" />
          <GtiStatus value={GTI_VALUE} delta={GTI_DELTA_1H} />
        </div>

        {/* Right: clock */}
        <div className="flex items-center gap-3 shrink-0">
          <div className="hidden sm:flex items-center gap-2">
            <span className="w-1.5 h-1.5 rounded-full bg-green-400 pulse-dot" />
            <span className="text-[10px] font-mono text-green-400 uppercase tracking-wider">LIVE</span>
          </div>
          <div className="hidden sm:block w-px h-5 bg-white/8" />
          <LiveClock />
        </div>
      </div>

      {/* Nav tabs */}
      <div className="flex border-t border-white/6 overflow-x-auto no-scrollbar">
        {TABS.map(({ id, label, sub, Icon }) => {
          const active = mode === id
          return (
            <button key={id} onClick={() => setMode(id)}
              className={`flex items-center gap-2 px-4 sm:px-6 py-2.5 border-b-2 transition-all whitespace-nowrap shrink-0
                ${active
                  ? 'border-sky-400 text-sky-400 bg-sky-400/5'
                  : 'border-transparent text-gray-400 hover:text-white hover:bg-white/3'
                }`}>
              <Icon className={`h-3.5 w-3.5 ${active ? 'text-sky-400' : ''}`} />
              <div className="text-left">
                <p className={`text-[11px] font-mono font-bold tracking-wider ${active ? 'text-sky-400' : ''}`}>{label}</p>
                <p className="text-[9px] text-gray-500 leading-none hidden sm:block">{sub}</p>
              </div>
            </button>
          )
        })}
      </div>
    </header>
  )
}
