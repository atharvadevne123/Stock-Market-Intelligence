import { useState, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ComposableMap, Geographies, Geography, Marker, ZoomableGroup } from 'react-simple-maps'
import { X } from 'lucide-react'
import { COUNTRIES, REGION_GTI, gtiColor } from '../../data/globe'

const GEO_URL = 'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json'

// ISO numeric → ISO alpha-2 lookup for the countries we care about
const NUMERIC_TO_ISO = {
  '004': 'AF', '008': 'AL', '012': 'DZ', '024': 'AO', '032': 'AR',
  '036': 'AU', '040': 'AT', '050': 'BD', '056': 'BE', '068': 'BO',
  '076': 'BR', '100': 'BG', '116': 'KH', '124': 'CA', '152': 'CL',
  '156': 'CN', '170': 'CO', '188': 'CR', '191': 'HR', '192': 'CU',
  '203': 'CZ', '208': 'DK', '218': 'EC', '818': 'EG', '231': 'ET',
  '246': 'FI', '250': 'FR', '276': 'DE', '288': 'GH', '300': 'GR',
  '320': 'GT', '340': 'HN', '348': 'HU', '356': 'IN', '360': 'ID',
  '364': 'IR', '368': 'IQ', '372': 'IE', '376': 'IL', '380': 'IT',
  '388': 'JM', '392': 'JP', '400': 'JO', '398': 'KZ', '404': 'KE',
  '408': 'KP', '410': 'KR', '414': 'KW', '422': 'LB', '458': 'MY',
  '484': 'MX', '504': 'MA', '528': 'NL', '554': 'NZ', '566': 'NG',
  '578': 'NO', '586': 'PK', '275': 'PS', '591': 'PA', '604': 'PE',
  '608': 'PH', '616': 'PL', '620': 'PT', '642': 'RO', '643': 'RU',
  '682': 'SA', '710': 'ZA', '724': 'ES', '752': 'SE', '756': 'CH',
  '760': 'SY', '158': 'TW', '764': 'TH', '792': 'TR', '800': 'UG',
  '804': 'UA', '784': 'AE', '826': 'GB', '840': 'US', '858': 'UY',
  '862': 'VE', '704': 'VN', '887': 'YE',
}

function getGti(geo) {
  const iso = NUMERIC_TO_ISO[geo.id] ?? geo.properties?.ISO_A2
  return COUNTRIES.find(c => c.iso === iso) ?? null
}

function CountryDetail({ country, onClose }) {
  const color = gtiColor(country.gti)
  const level = country.gti >= 80 ? 'CRITICAL' : country.gti >= 60 ? 'ELEVATED' : country.gti >= 40 ? 'MODERATE' : 'LOW'
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: 10 }}
      className="absolute bottom-4 left-4 w-64 bg-[#0a0f1e]/95 backdrop-blur-xl border border-white/12 rounded-xl overflow-hidden shadow-2xl z-20"
    >
      <div className="flex items-center justify-between px-4 py-3 border-b border-white/8">
        <div>
          <p className="text-[12px] font-semibold text-white">{country.name}</p>
          <p className="text-[9px] font-mono text-gray-500">{country.iso} · Geopolitical Snapshot</p>
        </div>
        <button onClick={onClose} className="text-gray-500 hover:text-white transition-colors">
          <X className="h-3.5 w-3.5" />
        </button>
      </div>
      <div className="p-4 space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-[9px] font-mono text-gray-500 uppercase tracking-widest">GTI Score</span>
          <div className="flex items-center gap-2">
            <span className="text-2xl font-mono font-bold" style={{ color }}>{country.gti}</span>
            <span className="text-[9px] font-mono px-1.5 py-0.5 rounded border"
              style={{ color, borderColor: color + '40', background: color + '15' }}>{level}</span>
          </div>
        </div>
        <div className="h-1.5 bg-white/8 rounded-full overflow-hidden">
          <div className="h-full rounded-full" style={{ width: `${country.gti}%`, background: color }} />
        </div>
        <div className="flex flex-wrap gap-1 pt-1">
          {['XAUUSD', 'USOIL', 'SPX', 'DXY'].slice(0, country.gti >= 60 ? 4 : 2).map(sym => (
            <span key={sym} className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-sky-500/10 border border-sky-500/20 text-sky-300">{sym}</span>
          ))}
        </div>
      </div>
    </motion.div>
  )
}

function RegionCard({ region }) {
  const textColor = region.score >= 80 ? 'text-red-400' : region.score >= 60 ? 'text-amber-400' : 'text-green-400'
  const barColor  = region.score >= 80 ? '#ef4444' : region.score >= 60 ? '#f59e0b' : '#22c55e'
  const deltaColor = region.delta >= 0 ? 'text-red-400' : 'text-green-400'
  return (
    <div className="bg-white/4 rounded-lg p-3 border border-white/8 hover:border-white/15 transition-colors">
      <div className="flex items-center justify-between mb-1.5">
        <span className="text-[11px] text-white font-mono">{region.region}</span>
        <div className="flex items-center gap-1.5">
          <span className={`text-[12px] font-mono font-bold ${textColor}`}>{region.score}</span>
          <span className={`text-[9px] font-mono ${deltaColor}`}>{region.delta >= 0 ? '+' : ''}{region.delta.toFixed(1)}</span>
        </div>
      </div>
      <div className="h-1 bg-white/8 rounded-full overflow-hidden mb-1">
        <div className="h-full rounded-full transition-all duration-700" style={{ width: `${region.score}%`, background: barColor }} />
      </div>
      <p className="text-[9px] text-gray-600">{region.driver} · {Math.round(region.weight * 100)}% weight</p>
    </div>
  )
}

export default function GeoMapView() {
  const [selected, setSelected] = useState(null)
  const [tooltipContent, setTooltipContent] = useState(null)

  return (
    <div className="flex h-full overflow-hidden">
      {/* Map area */}
      <div className="flex-1 relative bg-[#03060f] overflow-hidden">
        {/* Scanline */}
        <div className="absolute inset-0 pointer-events-none z-10 opacity-10"
          style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(14,165,233,0.04) 2px,rgba(14,165,233,0.04) 4px)' }} />

        <ComposableMap
          projection="geoMercator"
          projectionConfig={{ scale: 147, center: [10, 20] }}
          style={{ width: '100%', height: '100%', background: 'transparent' }}
        >
          <ZoomableGroup zoom={1} minZoom={0.8} maxZoom={6}>
            <Geographies geography={GEO_URL}>
              {({ geographies }) =>
                geographies.map(geo => {
                  const match = getGti(geo)
                  const baseColor = match ? gtiColor(match.gti) : '#1e293b'
                  const opacity = match ? (match.gti >= 80 ? 0.75 : match.gti >= 60 ? 0.6 : match.gti >= 40 ? 0.45 : 0.25) : 0.18
                  const isSelected = selected?.iso === match?.iso

                  return (
                    <Geography
                      key={geo.rsmKey}
                      geography={geo}
                      onClick={() => {
                        if (match) setSelected(prev => prev?.iso === match.iso ? null : match)
                      }}
                      onMouseEnter={() => match && setTooltipContent(match)}
                      onMouseLeave={() => setTooltipContent(null)}
                      style={{
                        default: {
                          fill: baseColor,
                          fillOpacity: opacity,
                          stroke: isSelected ? baseColor : 'rgba(255,255,255,0.08)',
                          strokeWidth: isSelected ? 1.5 : 0.4,
                          outline: 'none',
                          cursor: match ? 'pointer' : 'default',
                          transition: 'fill-opacity 0.2s',
                        },
                        hover: {
                          fill: match ? baseColor : '#334155',
                          fillOpacity: match ? Math.min(opacity + 0.2, 1) : 0.3,
                          stroke: match ? baseColor : 'rgba(255,255,255,0.15)',
                          strokeWidth: 0.8,
                          outline: 'none',
                        },
                        pressed: { outline: 'none' },
                      }}
                    />
                  )
                })
              }
            </Geographies>

            {/* High-risk country markers */}
            {COUNTRIES.filter(c => c.gti >= 65).map(c => (
              <Marker key={c.iso} coordinates={[c.lng, c.lat]}>
                <circle
                  r={c.gti >= 80 ? 4 : 3}
                  fill={gtiColor(c.gti)}
                  fillOpacity={0.9}
                  stroke="rgba(0,0,0,0.4)"
                  strokeWidth={0.5}
                  style={{ cursor: 'pointer' }}
                  onClick={() => setSelected(prev => prev?.iso === c.iso ? null : c)}
                />
                {c.gti >= 80 && (
                  <circle r={7} fill={gtiColor(c.gti)} fillOpacity={0.2} />
                )}
              </Marker>
            ))}
          </ZoomableGroup>
        </ComposableMap>

        {/* Hover tooltip */}
        {tooltipContent && (
          <div className="absolute top-4 left-1/2 -translate-x-1/2 pointer-events-none z-30
            bg-[#0a0f1e]/95 border border-white/15 rounded-lg px-3 py-2 text-center">
            <p className="text-[11px] font-mono font-semibold text-white">{tooltipContent.name}</p>
            <p className="text-[10px] font-mono mt-0.5" style={{ color: gtiColor(tooltipContent.gti) }}>
              GTI {tooltipContent.gti} · {tooltipContent.level.toUpperCase()}
            </p>
          </div>
        )}

        {/* Legend */}
        <div className="absolute top-4 right-4 bg-[#0a0f1e]/90 backdrop-blur-sm border border-white/10 rounded-lg p-3 z-20">
          <p className="text-[9px] font-mono uppercase tracking-widest text-gray-500 mb-2">Tension Level</p>
          {[
            { label: 'Critical (80+)', color: '#ef4444' },
            { label: 'High (60–80)',   color: '#f59e0b' },
            { label: 'Moderate (40+)', color: '#f97316' },
            { label: 'Low (<40)',      color: '#22c55e' },
          ].map(({ label, color }) => (
            <div key={label} className="flex items-center gap-2 mb-1">
              <div className="w-2.5 h-2.5 rounded-full" style={{ background: color }} />
              <span className="text-[10px] text-gray-400 font-mono">{label}</span>
            </div>
          ))}
          <p className="text-[8px] text-gray-600 mt-2 font-mono">Scroll to zoom · Drag to pan</p>
        </div>

        {/* Country detail popup */}
        <AnimatePresence>
          {selected && <CountryDetail country={selected} onClose={() => setSelected(null)} />}
        </AnimatePresence>
      </div>

      {/* Right panel */}
      <div className="w-72 shrink-0 border-l border-white/8 overflow-y-auto p-4 space-y-3 hidden lg:block">
        <p className="text-[9px] font-mono uppercase tracking-widest text-gray-500 mb-1">Regional GTI Breakdown</p>
        {REGION_GTI.map(r => <RegionCard key={r.region} region={r} />)}

        <div className="mt-2 pt-2">
          <p className="text-[9px] font-mono uppercase tracking-widest text-gray-500 mb-2">High-Risk Countries</p>
          <div className="space-y-1.5">
            {COUNTRIES
              .filter(c => c.gti >= 70)
              .sort((a, b) => b.gti - a.gti)
              .map(c => (
                <div
                  key={c.iso}
                  className="flex items-center justify-between px-2.5 py-1.5 rounded-lg bg-white/3 border border-white/6 cursor-pointer hover:border-white/15 transition-colors"
                  onClick={() => setSelected(prev => prev?.iso === c.iso ? null : c)}
                >
                  <div className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full" style={{ background: gtiColor(c.gti) }} />
                    <span className="text-[11px] text-gray-300">{c.name}</span>
                  </div>
                  <span className="text-[10px] font-mono" style={{ color: gtiColor(c.gti) }}>{c.gti}</span>
                </div>
              ))}
          </div>
        </div>
      </div>
    </div>
  )
}
