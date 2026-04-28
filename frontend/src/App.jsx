import { useState } from 'react'
import Header from './components/Header'
import GlobeView from './components/globe/GlobeView'
import GeoMapView from './components/map/GeoMapView'
import SignalsView from './components/signals/SignalsView'
import PortfolioView from './components/portfolio/PortfolioView'
import Sidebar from './components/Sidebar'
import { useStore } from './store'

export default function App() {
  const { mode, sidebarOpen, setSidebarOpen } = useStore()

  return (
    <div className="flex flex-col h-screen bg-[#07091a] overflow-hidden">
      <Header onMenuToggle={() => setSidebarOpen(!sidebarOpen)} menuOpen={sidebarOpen} />

      <div className="flex flex-1 overflow-hidden relative">
        {/* Sidebar */}
        <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />

        {/* Main content */}
        <main className="flex-1 overflow-hidden relative">
          {mode === 'globe'     && <GlobeView />}
          {mode === 'map'       && <GeoMapView />}
          {mode === 'charts'    && <SignalsView />}
          {mode === 'portfolio' && <PortfolioView />}
        </main>
      </div>
    </div>
  )
}
