import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import PortfolioPage from './pages/PortfolioPage';
import MarketPage from './pages/MarketPage';

function App() {
  return (
    <Router>
      <div className="app">
        <Navbar />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/portfolio" element={<PortfolioPage />} />
          <Route path="/market" element={<MarketPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
