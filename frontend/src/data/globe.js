export const COUNTRIES = [
  { iso: "RU", name: "Russia",        lat: 61.52, lng: 105.31, gti: 92, level: "critical" },
  { iso: "UA", name: "Ukraine",       lat: 48.37, lng: 31.16,  gti: 88, level: "critical" },
  { iso: "IL", name: "Israel",        lat: 31.04, lng: 34.85,  gti: 85, level: "critical" },
  { iso: "IR", name: "Iran",          lat: 32.42, lng: 53.68,  gti: 82, level: "critical" },
  { iso: "KP", name: "North Korea",   lat: 40.33, lng: 127.51, gti: 80, level: "critical" },
  { iso: "YE", name: "Yemen",         lat: 15.55, lng: 48.51,  gti: 78, level: "high" },
  { iso: "SY", name: "Syria",         lat: 34.80, lng: 38.99,  gti: 75, level: "high" },
  { iso: "IQ", name: "Iraq",          lat: 33.22, lng: 43.67,  gti: 72, level: "high" },
  { iso: "AF", name: "Afghanistan",   lat: 33.93, lng: 67.70,  gti: 70, level: "high" },
  { iso: "MM", name: "Myanmar",       lat: 21.91, lng: 95.95,  gti: 62, level: "medium" },
  { iso: "VE", name: "Venezuela",     lat: 6.42,  lng: -66.58, gti: 58, level: "medium" },
  { iso: "PK", name: "Pakistan",      lat: 30.37, lng: 69.34,  gti: 52, level: "medium" },
  { iso: "CN", name: "China",         lat: 35.86, lng: 104.19, gti: 50, level: "medium" },
  { iso: "NG", name: "Nigeria",       lat: 9.08,  lng: 8.67,   gti: 42, level: "medium" },
  { iso: "ZA", name: "South Africa",  lat: -30.55, lng: 22.93, gti: 40, level: "medium" },
  { iso: "EG", name: "Egypt",         lat: 26.82, lng: 30.80,  gti: 40, level: "medium" },
  { iso: "MX", name: "Mexico",        lat: 23.63, lng: -102.55,gti: 38, level: "low" },
  { iso: "IN", name: "India",         lat: 20.59, lng: 78.96,  gti: 35, level: "low" },
  { iso: "PL", name: "Poland",        lat: 51.91, lng: 19.14,  gti: 30, level: "low" },
  { iso: "AE", name: "UAE",           lat: 23.42, lng: 53.84,  gti: 30, level: "low" },
  { iso: "KR", name: "South Korea",   lat: 35.90, lng: 127.76, gti: 35, level: "low" },
  { iso: "SA", name: "Saudi Arabia",  lat: 23.88, lng: 45.07,  gti: 28, level: "low" },
  { iso: "TR", name: "Turkey",        lat: 38.96, lng: 35.24,  gti: 45, level: "medium" },
  { iso: "US", name: "United States", lat: 37.09, lng: -95.71, gti: 22, level: "low" },
  { iso: "DE", name: "Germany",       lat: 51.16, lng: 10.45,  gti: 20, level: "low" },
  { iso: "GB", name: "UK",            lat: 55.37, lng: -3.43,  gti: 18, level: "low" },
  { iso: "JP", name: "Japan",         lat: 36.20, lng: 138.25, gti: 25, level: "low" },
  { iso: "BR", name: "Brazil",        lat: -14.23, lng: -51.92,gti: 32, level: "low" },
  { iso: "CA", name: "Canada",        lat: 56.13, lng: -106.34,gti: 15, level: "low" },
  { iso: "AU", name: "Australia",     lat: -25.27, lng: 133.77,gti: 15, level: "low" },
]

export const ARCS = [
  { startLat: 61.52, startLng: 105.31, endLat: 48.37, endLng: 31.16,  type: "military_escalation", severity: 0.95, from: "Russia",        to: "Ukraine",      color: ["rgba(239,68,68,0.9)","rgba(220,38,38,0.7)"] },
  { startLat: 32.42, startLng: 53.68,  endLat: 31.04, endLng: 34.85,  type: "military_escalation", severity: 0.88, from: "Iran",          to: "Israel",       color: ["rgba(239,68,68,0.9)","rgba(220,38,38,0.7)"] },
  { startLat: 37.09, startLng: -95.71, endLat: 32.42, endLng: 53.68,  type: "sanctions",            severity: 0.80, from: "United States", to: "Iran",         color: ["rgba(249,115,22,0.9)","rgba(239,68,68,0.7)"] },
  { startLat: 37.09, startLng: -95.71, endLat: 61.52, endLng: 105.31, type: "sanctions",            severity: 0.85, from: "United States", to: "Russia",       color: ["rgba(249,115,22,0.9)","rgba(239,68,68,0.7)"] },
  { startLat: 37.09, startLng: -95.71, endLat: 35.86, endLng: 104.19, type: "trade_restrictions",   severity: 0.72, from: "United States", to: "China",        color: ["rgba(245,158,11,0.8)","rgba(234,179,8,0.7)"] },
  { startLat: 35.86, startLng: 104.19, endLat: 20.59, endLng: 78.96,  type: "diplomatic_activity",  severity: 0.55, from: "China",         to: "India",        color: ["rgba(14,165,233,0.7)","rgba(99,102,241,0.6)"] },
  { startLat: 23.88, startLng: 45.07,  endLat: 15.55, endLng: 48.51,  type: "military_escalation",  severity: 0.75, from: "Saudi Arabia",  to: "Yemen",        color: ["rgba(239,68,68,0.9)","rgba(220,38,38,0.7)"] },
  { startLat: 40.33, startLng: 127.51, endLat: 35.90, endLng: 127.76, type: "military_escalation",  severity: 0.70, from: "North Korea",   to: "South Korea",  color: ["rgba(239,68,68,0.9)","rgba(220,38,38,0.7)"] },
]

export const EVENTS = [
  { id: "e1", lat: 32,  lng: 35,   title: "Middle East Escalation",         severity: 0.90, type: "military_escalation", region: "IL", ago: "1h ago" },
  { id: "e2", lat: 50,  lng: 30,   title: "Ukraine Conflict Intensifies",   severity: 0.85, type: "military_escalation", region: "UA", ago: "2h ago" },
  { id: "e3", lat: 39,  lng: 126,  title: "DPRK Missile Test",              severity: 0.78, type: "military_escalation", region: "KP", ago: "4h ago" },
  { id: "e4", lat: 25,  lng: 55,   title: "Strait of Hormuz Naval Activity",severity: 0.80, type: "military_escalation", region: "AE", ago: "6h ago" },
]

export const REGION_GTI = [
  { region: "Middle East",   score: 84, driver: "Conflict",       weight: 0.40, delta: +2.1 },
  { region: "Asia Pacific",  score: 62, driver: "Trade Tensions", weight: 0.30, delta: +0.8 },
  { region: "Europe",        score: 71, driver: "War Spillover",  weight: 0.20, delta: -0.3 },
  { region: "North America", score: 22, driver: "Policy",         weight: 0.05, delta: +0.1 },
  { region: "Latin America", score: 35, driver: "Political",      weight: 0.03, delta: -0.2 },
  { region: "Africa",        score: 40, driver: "Instability",    weight: 0.02, delta: +0.0 },
]

export const GTI_VALUE    = 67.4
export const GTI_DELTA_1H = +1.8

export function gtiColor(score) {
  if (score >= 80) return "#ef4444"
  if (score >= 60) return "#f59e0b"
  if (score >= 40) return "#f97316"
  return "#22c55e"
}

export function gtiOpacity(score) {
  return Math.max(0.08, score / 100 * 0.75)
}
