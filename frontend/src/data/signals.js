export const SIGNALS = [
  {
    asset: "GOLD (XAUUSD)", assetClass: "commodity", action: "BUY",
    confidence: 88, uncertainty: 8,
    price: "$2,340", change: "+1.4%", changeDir: 1,
    summary: "Safe-haven demand increasing due to Middle East escalation and rising global tension index.",
    trigger: "Iran-Israel Missile Exchange — Severity 0.88",
    path: ["Middle East Conflict", "Safe Haven Demand", "Gold Price"],
    chain: [
      { step: 1, desc: "GTI elevated to 85 in Middle East region",          evidence: "Multiple conflict signals detected past 6h",     conf: 0.35 },
      { step: 2, desc: "Historical: GTI >80 → Gold +3.2% avg",              evidence: "Backtested over 847 similar events",             conf: 0.28 },
      { step: 3, desc: "USD weakening trend supports commodity rally",       evidence: "DXY -0.4% in past session",                     conf: 0.23 },
    ],
  },
  {
    asset: "CRUDE OIL (WTI)", assetClass: "commodity", action: "BUY",
    confidence: 79, uncertainty: 14,
    price: "$82.40", change: "+0.8%", changeDir: 1,
    summary: "Supply disruption risk from Strait of Hormuz activity driving oil premium.",
    trigger: "Naval Drills Near Strait of Hormuz — Severity 0.80",
    path: ["Iran Tension", "Hormuz Supply Risk", "Oil Price"],
    chain: [
      { step: 1, desc: "Naval activity near Hormuz detected",               evidence: "GDELT conflict events: 14 in past 4h",           conf: 0.40 },
      { step: 2, desc: "20% global oil supply transits Hormuz",             evidence: "EIA supply route data",                         conf: 0.25 },
      { step: 3, desc: "OPEC+ spare capacity limited",                      evidence: "Current utilization >92%",                      conf: 0.14 },
    ],
  },
  {
    asset: "S&P 500 (SPX)", assetClass: "equity", action: "SELL",
    confidence: 72, uncertainty: 18,
    price: "$5,204", change: "-0.6%", changeDir: -1,
    summary: "Risk premium expansion and sector rotation into defensives amid geopolitical uncertainty.",
    trigger: "US-Russia Sanctions Escalation — Severity 0.85",
    path: ["Geopolitical Risk", "Risk Premium", "Equity Valuations"],
    chain: [
      { step: 1, desc: "Global GTI at 67.4 — historically bearish for equities", evidence: "Historical win rate: 68% SELL signals at GTI >65", conf: 0.30 },
      { step: 2, desc: "VIX elevated, options market pricing uncertainty",   evidence: "VIX at 22.4, above 30-day avg of 16.8",          conf: 0.22 },
      { step: 3, desc: "Tech sector vulnerable to supply chain disruption",  evidence: "Taiwan Strait affecting semiconductor supply",   conf: 0.20 },
    ],
  },
  {
    asset: "WHEAT FUTURES", assetClass: "commodity", action: "BUY",
    confidence: 68, uncertainty: 22,
    price: "$582", change: "+2.1%", changeDir: 1,
    summary: "Ukraine conflict disrupting Black Sea grain exports; supply shock likely to persist.",
    trigger: "Ukraine Black Sea Shipping Disruption — Severity 0.88",
    path: ["Ukraine Conflict", "Black Sea Export Disruption", "Wheat Price"],
    chain: [
      { step: 1, desc: "Ukraine + Russia supply ~30% of global wheat exports", evidence: "UN FAO trade data 2024",                        conf: 0.38 },
      { step: 2, desc: "Shipping insurance premiums spiking in Black Sea",    evidence: "+340% premium increase vs pre-conflict",         conf: 0.18 },
      { step: 3, desc: "Alternative supply routes insufficient to offset",    evidence: "Argentina and Australia crop yield below avg",   conf: 0.12 },
    ],
  },
  {
    asset: "USD/JPY", assetClass: "currency", action: "SELL",
    confidence: 61, uncertainty: 25,
    price: "154.22", change: "-0.3%", changeDir: -1,
    summary: "JPY safe-haven flows increasing; Bank of Japan intervention risk elevated.",
    trigger: "North Korea DPRK Missile Test — Severity 0.78",
    path: ["DPRK Escalation", "Asia Safe Haven Flows", "JPY Strength"],
    chain: [
      { step: 1, desc: "Historical: DPRK events → JPY +0.8% avg within 24h", evidence: "15 similar events since 2016",                  conf: 0.28 },
      { step: 2, desc: "BOJ signaling readiness for FX intervention",         evidence: "Verbal intervention at 155.00 level",           conf: 0.20 },
      { step: 3, desc: "Position unwind from carry trade risk",               evidence: "Large short JPY positions outstanding",         conf: 0.13 },
    ],
  },
  {
    asset: "NATURAL GAS (NATGAS)", assetClass: "commodity", action: "HOLD",
    confidence: 55, uncertainty: 30,
    price: "$3.18", change: "+0.2%", changeDir: 1,
    summary: "European storage above seasonal norms offsetting Russia supply risk. Mixed signals.",
    trigger: "Russia-EU Energy Dispute — Severity 0.65",
    path: ["Russia Sanctions", "EU Energy Security", "Gas Storage Levels"],
    chain: [
      { step: 1, desc: "EU gas storage at 68% — above 5-year avg of 55%",  evidence: "GIE AGSI+ storage data",                        conf: 0.20 },
      { step: 2, desc: "LNG imports from US compensating pipeline shortfall",evidence: "US LNG export capacity at record",              conf: 0.18 },
      { step: 3, desc: "Demand uncertainty with mild winter forecast",       evidence: "NOAA weather models",                          conf: 0.10 },
    ],
  },
]

export const NLP_STATS = {
  articles_processed: 2847,
  sentiment_score: -0.34,
  macro_narratives: 12,
  top_topics: ["Iran-Israel", "Russia-Ukraine", "DPRK Missile", "Oil Supply", "USD Weakness"],
}

export const GTI_HISTORY = Array.from({ length: 48 }, (_, i) => ({
  hour: i,
  value: 60 + Math.sin(i / 6) * 8 + Math.random() * 4 + (i > 40 ? 5 : 0),
}))
