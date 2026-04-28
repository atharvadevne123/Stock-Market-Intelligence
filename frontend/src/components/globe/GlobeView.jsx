import { useRef, useCallback, useState, useEffect } from 'react'
import Globe from 'react-globe.gl'
import { motion, AnimatePresence } from 'framer-motion'
import { X, AlertTriangle, Shield, Activity } from 'lucide-react'
import { COUNTRIES, ARCS, EVENTS, gtiColor, gtiOpacity } from '../../data/globe'
import { useStore } from '../../store'

const TYPE_LABELS = {
  military_escalation: 'Military',
  trade_restrictions: 'Trade',
  sanctions: 'Sanctions',
  diplomatic_activity: 'Diplomatic',
}

const TYPE_COLORS = {
  military_escalation: 'text-red-400 bg-red-500/10 border-red-500/20',
  trade_restrictions:  'text-amber-400 bg-amber-500/10 border-amber-500/20',
  sanctions:           'text-orange-400 bg-orange-500/10 border-orange-500/20',
  diplomatic_activity: 'text-sky-400 bg-sky-500/10 border-sky-500/20',
}

function CountryPanel({ country, onClose }) {
  if (!country) return null
  const color = country.gti >= 80 ? 'text-red-400' : country.gti >= 60 ? 'text-amber-400' : country.gti >= 40 ? 'text-orange-400' : 'text-green-400'
  const level = country.gti >= 80 ? 'CRITICAL' : country.gti >= 60 ? 'ELEVATED' : country.gti >= 40 ? 'MODERATE' : 'LOW'
  const levelBg = country.gti >= 80 ? 'bg-red-500/10 border-red-500/30' : country.gti >= 60 ? 'bg-amber-500/10 border-amber-500/30' : country.gti >= 40 ? 'bg-orange-500/10 border-orange-500/30' : 'bg-green-500/10 border-green-500/30'

  const relevantArcs = ARCS.filter(a => a.from === country.name || a.to === country.name)

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 20 }}
      className="absolute right-4 top-4 w-72 bg-[#0a0f1e]/95 backdrop-blur-xl border border-white/12 rounded-xl overflow-hidden shadow-2xl z-20"
    >
      <div className="flex items-center justify-between px-4 py-3 border-b border-white/8">
        <div>
          <p className="text-sm font-semibold text-white">{country.name}</p>
          <p className="text-[10px] font-mono text-gray-500 mt-0.5">{country.iso} · Geopolitical Profile</p>
        </div>
        <button onClick={onClose} className="text-gray-500 hover:text-white transition-colors">
          <X className="h-4 w-4" />
        </button>
      </div>

      <div className="p-4 space-y-4">
        {/* GTI Score */}
        <div className={`rounded-lg border p-3 ${levelBg}`}>
          <p className="text-[9px] font-mono uppercase tracking-widest text-gray-500 mb-1">GTI Score</p>
          <div className="flex items-end gap-2">
            <span className={`text-3xl font-mono font-bold ${color}`}>{country.gti}</span>
            <span className={`text-[10px] font-mono mb-1 px-1.5 py-0.5 rounded border ${levelBg} ${color}`}>{level}</span>
          </div>
          <div className="h-1.5 bg-black/30 rounded-full mt-2 overflow-hidden">
            <div className="h-full rounded-full" style={{ width: `${country.gti}%`, background: gtiColor(country.gti) }} />
          </div>
        </div>

        {/* Conflict arcs */}
        {relevantArcs.length > 0 && (
          <div>
            <p className="text-[9px] font-mono uppercase tracking-widest text-gray-500 mb-2">Active Conflicts</p>
            <div className="space-y-2">
              {relevantArcs.map((arc, i) => (
                <div key={i} className="flex items-center justify-between text-xs">
                  <div className="flex items-center gap-1.5">
                    <span className={`text-[9px] px-1.5 py-0.5 rounded border font-mono ${TYPE_COLORS[arc.type] ?? 'text-gray-400 bg-white/5 border-white/10'}`}>
                      {TYPE_LABELS[arc.type] ?? arc.type}
                    </span>
                    <span className="text-gray-400">{arc.from === country.name ? `→ ${arc.to}` : `← ${arc.from}`}</span>
                  </div>
                  <span className="font-mono text-[10px] text-white">{(arc.severity * 100).toFixed(0)}%</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Affected assets */}
        <div>
          <p className="text-[9px] font-mono uppercase tracking-widest text-gray-500 mb-2">Market Exposure</p>
          <div className="flex flex-wrap gap-1.5">
            {['XAUUSD','USOIL','SPX','DXY'].slice(0, country.gti >= 60 ? 4 : 2).map(sym => (
              <span key={sym} className="text-[10px] font-mono px-2 py-0.5 rounded bg-sky-500/10 border border-sky-500/20 text-sky-300">{sym}</span>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  )
}

export default function GlobeView() {
  const globeRef = useRef()
  const containerRef = useRef()
  const { selectedCountry, setSelectedCountry } = useStore()
  const [dimensions, setDimensions] = useState({ w: 800, h: 600 })
  const [countries, setCountries] = useState({ features: [] })

  useEffect(() => {
    const measure = () => {
      if (containerRef.current) {
        const { offsetWidth, offsetHeight } = containerRef.current
        setDimensions({ w: offsetWidth, h: offsetHeight })
      }
    }
    measure()
    const ro = new ResizeObserver(measure)
    if (containerRef.current) ro.observe(containerRef.current)
    return () => ro.disconnect()
  }, [])

  // Load countries GeoJSON for coloring
  useEffect(() => {
    fetch('https://raw.githubusercontent.com/vasturiano/react-globe.gl/master/example/datasets/ne_110m_admin_0_countries.geojson')
      .then(r => r.json())
      .then(data => setCountries(data))
      .catch(() => setCountries({ features: [] }))
  }, [])

  // Point to globe on load
  useEffect(() => {
    if (globeRef.current) {
      globeRef.current.controls().autoRotate = true
      globeRef.current.controls().autoRotateSpeed = 0.3
      globeRef.current.pointOfView({ lat: 25, lng: 20, altitude: 2.2 }, 1500)
    }
  }, [])

  const handleCountryClick = useCallback((feat) => {
    const iso = feat?.properties?.ISO_A2
    const match = COUNTRIES.find(c => c.iso === iso)
    if (match) {
      setSelectedCountry(match)
      if (globeRef.current) {
        globeRef.current.controls().autoRotate = false
        globeRef.current.pointOfView({ lat: match.lat, lng: match.lng, altitude: 1.8 }, 800)
      }
    }
  }, [setSelectedCountry])

  const polygonColor = useCallback((feat) => {
    const iso = feat?.properties?.ISO_A2
    const match = COUNTRIES.find(c => c.iso === iso)
    if (match) return `rgba(${hexToRgb(gtiColor(match.gti))},${gtiOpacity(match.gti)})`
    return 'rgba(255,255,255,0.03)'
  }, [])

  const polygonStroke = useCallback((feat) => {
    const iso = feat?.properties?.ISO_A2
    const match = COUNTRIES.find(c => c.iso === iso)
    if (match && match.gti >= 60) return gtiColor(match.gti)
    return 'rgba(255,255,255,0.06)'
  }, [])

  return (
    <div ref={containerRef} className="relative w-full h-full overflow-hidden bg-[#03060f]">
      {/* Scanline overlay */}
      <div className="absolute inset-0 pointer-events-none z-10 opacity-20"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(14,165,233,0.03) 2px,rgba(14,165,233,0.03) 4px)' }} />

      <Globe
        ref={globeRef}
        width={dimensions.w}
        height={dimensions.h}
        backgroundColor="#03060f"
        globeImageUrl="//unpkg.com/three-globe/example/img/earth-night.jpg"
        bumpImageUrl="//unpkg.com/three-globe/example/img/earth-topology.png"
        atmosphereColor="#0ea5e9"
        atmosphereAltitude={0.12}
        polygonsData={countries.features}
        polygonCapColor={polygonColor}
        polygonSideColor={() => 'rgba(0,0,0,0.1)'}
        polygonStrokeColor={polygonStroke}
        polygonAltitude={feat => {
          const iso = feat?.properties?.ISO_A2
          const match = COUNTRIES.find(c => c.iso === iso)
          return match && match.gti >= 60 ? 0.008 : 0.001
        }}
        onPolygonClick={handleCountryClick}
        polygonLabel={feat => {
          const iso = feat?.properties?.ISO_A2
          const match = COUNTRIES.find(c => c.iso === iso)
          if (!match) return feat?.properties?.NAME ?? ''
          return `<div style="font-family:monospace;background:#0a0f1e;border:1px solid rgba(255,255,255,0.15);padding:8px 12px;border-radius:6px;color:#e2e8f0">
            <b>${match.name}</b><br/>
            <span style="color:${gtiColor(match.gti)}">GTI: ${match.gti} · ${match.level.toUpperCase()}</span>
          </div>`
        }}
        arcsData={ARCS}
        arcStartLat="startLat" arcStartLng="startLng"
        arcEndLat="endLat"   arcEndLng="endLng"
        arcColor="color"
        arcDashLength={0.4}
        arcDashGap={0.15}
        arcDashAnimateTime={1800}
        arcStroke={a => a.severity * 0.8}
        arcAltitudeAutoScale={0.4}
        pointsData={EVENTS}
        pointLat="lat" pointLng="lng"
        pointColor={p => p.severity >= 0.85 ? '#ef4444' : p.severity >= 0.70 ? '#f59e0b' : '#22c55e'}
        pointAltitude={0.02}
        pointRadius={p => p.severity * 0.6}
        pointLabel={p => `<div style="font-family:monospace;background:#0a0f1e;border:1px solid rgba(255,255,255,0.15);padding:8px 12px;border-radius:6px;color:#e2e8f0">
          <b>${p.title}</b><br/>
          <span style="color:#ef4444">Severity: ${(p.severity * 100).toFixed(0)}%</span>
        </div>`}
      />

      {/* Country panel */}
      <AnimatePresence>
        {selectedCountry && (
          <CountryPanel country={selectedCountry} onClose={() => {
            setSelectedCountry(null)
            if (globeRef.current) globeRef.current.controls().autoRotate = true
          }} />
        )}
      </AnimatePresence>

      {/* Legend */}
      <div className="absolute bottom-4 left-4 bg-[#0a0f1e]/90 backdrop-blur-sm border border-white/10 rounded-lg p-3 z-20">
        <p className="text-[9px] font-mono uppercase tracking-widest text-gray-500 mb-2">Tension Level</p>
        {[
          { label: 'Critical (80+)', color: '#ef4444' },
          { label: 'High (60–80)',   color: '#f59e0b' },
          { label: 'Moderate (40+)', color: '#f97316' },
          { label: 'Low (<40)',      color: '#22c55e' },
        ].map(({ label, color }) => (
          <div key={label} className="flex items-center gap-2 mb-1">
            <div className="w-3 h-1.5 rounded-full" style={{ background: color }} />
            <span className="text-[10px] text-gray-400 font-mono">{label}</span>
          </div>
        ))}
        <div className="mt-2 pt-2 border-t border-white/8">
          <p className="text-[9px] font-mono uppercase tracking-widest text-gray-500 mb-1">Arc Types</p>
          <div className="flex items-center gap-2">
            <div className="w-8 h-0.5 bg-red-400 opacity-80" style={{ backgroundImage: 'repeating-linear-gradient(90deg,#ef4444 0,#ef4444 4px,transparent 4px,transparent 8px)' }} />
            <span className="text-[9px] text-gray-400 font-mono">Conflict</span>
          </div>
          <div className="flex items-center gap-2 mt-0.5">
            <div className="w-8 h-0.5 bg-amber-400 opacity-80" style={{ backgroundImage: 'repeating-linear-gradient(90deg,#f59e0b 0,#f59e0b 4px,transparent 4px,transparent 8px)' }} />
            <span className="text-[9px] text-gray-400 font-mono">Trade/Sanctions</span>
          </div>
        </div>
      </div>

      {/* Event list overlay */}
      <div className="absolute bottom-4 right-4 w-60 bg-[#0a0f1e]/90 backdrop-blur-sm border border-white/10 rounded-lg overflow-hidden z-20">
        <div className="px-3 py-2 border-b border-white/8">
          <p className="text-[9px] font-mono uppercase tracking-widest text-gray-500">Live Events ({EVENTS.length})</p>
        </div>
        {EVENTS.map(ev => (
          <div key={ev.id} className="flex items-start gap-2 px-3 py-2 border-b border-white/5 last:border-0 hover:bg-white/3 transition-colors">
            <div className="w-1.5 h-1.5 rounded-full mt-1.5 shrink-0 pulse-dot"
              style={{ background: ev.severity >= 0.85 ? '#ef4444' : ev.severity >= 0.70 ? '#f59e0b' : '#22c55e' }} />
            <div className="min-w-0">
              <p className="text-[11px] text-white leading-tight truncate">{ev.title}</p>
              <div className="flex items-center gap-1.5 mt-0.5">
                <span className="text-[9px] font-mono text-red-400">{(ev.severity * 100).toFixed(0)}%</span>
                <span className="text-[9px] text-gray-600">{ev.ago}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

function hexToRgb(hex) {
  const r = parseInt(hex.slice(1,3),16), g = parseInt(hex.slice(3,5),16), b = parseInt(hex.slice(5,7),16)
  return `${r},${g},${b}`
}
