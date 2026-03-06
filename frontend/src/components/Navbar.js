import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          📈 Stock Market Intelligence
        </Link>
        <div className="navbar-menu">
          <Link to="/" className="nav-link">Dashboard</Link>
          <Link to="/portfolio" className="nav-link">Portfolio</Link>
          <Link to="/market" className="nav-link">Market</Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
