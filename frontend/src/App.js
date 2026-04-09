import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './index.css';
import DashboardPage from './pages/DashboardPage';
import TickerPage from './pages/TickerPage';
import PortfolioPage from './pages/PortfolioPage';
import MarketPage from './pages/MarketPage';
import SignalsPage from './pages/SignalsPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/ticker/nvda" element={<TickerPage />} />
        <Route path="/portfolio" element={<PortfolioPage />} />
        <Route path="/market" element={<MarketPage />} />
        <Route path="/signals" element={<SignalsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
