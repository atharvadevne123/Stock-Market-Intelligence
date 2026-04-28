import { create } from 'zustand'
import { GTI_VALUE } from './data/globe'

// Weights: how much each scenario factor moves each asset (% per 100 slider units)
const IMPACT_MATRIX = {
  //              oilShock  rateChange  escalation  supplyChain  cyberThreat
  XAUUSD:       [  +2.0,     -0.8,       +3.5,       +0.5,        +1.2 ],
  'USOIL/WTI':  [  +8.0,     -0.5,       +4.0,       +1.5,        +0.3 ],
  'SPX':        [  -3.5,     -4.0,       -4.5,       -2.5,        -3.0 ],
  'DXY':        [  -1.0,     +3.5,       -1.5,       -0.5,        -1.0 ],
  'USD/JPY':    [  +0.5,     +2.0,       -2.5,       -0.3,        -0.8 ],
  'WHEAT':      [  +1.5,     -0.3,       +2.0,       +3.5,        +0.2 ],
  'NATGAS':     [  +4.0,     -0.4,       +2.5,       +1.0,        +0.5 ],
  'BONDS/TLT':  [  -0.5,     -5.0,       +2.0,       +0.5,        +1.5 ],
}

// How much each factor moves global GTI (per 100 units)
const GTI_WEIGHTS = { oilShock: 8, rateChange: 4, escalation: 15, supplyChain: 6, cyberThreat: 7 }

function runSimulationEngine(scenario) {
  const factors = [
    scenario.oilShock / 100,
    scenario.rateChange / 100,
    scenario.escalation / 100,
    scenario.supplyChain / 100,
    scenario.cyberThreat / 100,
  ]

  // Adjusted GTI
  const gtiDelta = Object.entries(GTI_WEIGHTS).reduce((sum, [key, w], i) =>
    sum + (scenario[Object.keys(GTI_WEIGHTS)[i]] - (key === 'escalation' ? 50 : key === 'supplyChain' ? 30 : key === 'cyberThreat' ? 40 : 0)) / 100 * w
  , 0)
  const adjustedGti = Math.min(100, Math.max(0, GTI_VALUE + gtiDelta))

  // Asset impacts
  const assets = Object.entries(IMPACT_MATRIX).map(([asset, weights]) => {
    const pct = weights.reduce((sum, w, i) => sum + w * factors[i], 0)
    return {
      asset,
      pct: +pct.toFixed(1),
      action: pct >= 1.5 ? 'BUY' : pct <= -1.5 ? 'SELL' : 'HOLD',
    }
  }).sort((a, b) => Math.abs(b.pct) - Math.abs(a.pct))

  // Top alerts
  const alerts = []
  if (scenario.escalation > 70) alerts.push('Geopolitical escalation above threshold — safe-haven demand elevated')
  if (scenario.oilShock > 60)   alerts.push('Oil shock scenario — energy sector and transport under pressure')
  if (scenario.rateChange > 60) alerts.push('Rate hike path — bond prices falling, USD strengthening')
  if (scenario.supplyChain > 65) alerts.push('Supply chain stress — agricultural commodities and tech at risk')
  if (scenario.cyberThreat > 70) alerts.push('Elevated cyber threat — financial sector volatility expected')

  return { adjustedGti, gtiDelta: +gtiDelta.toFixed(1), assets, alerts }
}

export const useStore = create((set) => ({
  mode: 'globe',
  setMode: (mode) => set({ mode }),

  selectedCountry: null,
  setSelectedCountry: (country) => set({ selectedCountry: country }),

  selectedRegions: [],
  toggleRegion: (region) => set((s) => ({
    selectedRegions: s.selectedRegions.includes(region)
      ? s.selectedRegions.filter(r => r !== region)
      : [...s.selectedRegions, region]
  })),

  scenario: {
    oilShock: 0,
    rateChange: 0,
    escalation: 50,
    supplyChain: 30,
    cyberThreat: 40,
  },
  updateScenario: (key, val) => set((s) => ({ scenario: { ...s.scenario, [key]: val } })),

  simResults: null,
  runSimulation: () => set((s) => ({ simResults: runSimulationEngine(s.scenario) })),
  clearSimResults: () => set({ simResults: null }),

  expandedSignal: null,
  setExpandedSignal: (id) => set((s) => ({ expandedSignal: s.expandedSignal === id ? null : id })),

  sidebarOpen: false,
  setSidebarOpen: (v) => set({ sidebarOpen: v }),
}))
