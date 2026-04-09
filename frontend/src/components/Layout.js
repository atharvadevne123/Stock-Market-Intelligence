import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

const Layout = ({ children }) => {
  const location = useLocation();
  const [userMenuOpen, setUserMenuOpen] = useState(false);

  const isActive = (path) => location.pathname === path;

  const navItems = [
    { path: '/', icon: 'dashboard', label: 'Dashboard' },
    { path: '/ticker/nvda', icon: 'memory', label: 'NVDA Analysis' },
    { path: '/portfolio', icon: 'account_balance_wallet', label: 'Portfolio' },
    { path: '/market', icon: 'map', label: 'Market Map' },
    { path: '/signals', icon: 'sensors', label: 'Signals' },
    { path: '/settings', icon: 'settings', label: 'Settings' },
  ];

  return (
    <div className="dark bg-surface text-on-surface font-body min-h-screen flex">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 h-screen w-64 border-r border-outline-variant/30 bg-surface shadow-sidebar z-50 flex flex-col">
        <div className="p-6">
          <div className="text-xl font-bold text-primary tracking-widest uppercase font-headline">
            Sovereign Terminal
          </div>
          <div className="text-[10px] text-on-surface-variant/60 tracking-[0.2em] uppercase mt-1">
            Institutional Grade
          </div>
        </div>

        <nav className="flex-1 mt-4">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-3 px-6 py-3 transition-all ${
                isActive(item.path)
                  ? 'text-primary bg-surface-container-low border-r-2 border-primary'
                  : 'text-on-surface-variant/60 hover:bg-surface-container-low hover:text-on-surface'
              }`}
            >
              <span className="material-symbols-outlined">{item.icon}</span>
              <span className="text-sm font-medium">{item.label}</span>
            </Link>
          ))}
        </nav>

        <div className="p-4 bg-surface-container-low mx-4 mb-6 rounded-lg border border-outline-variant/10">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full overflow-hidden bg-surface-container-highest">
              <img
                alt="User Profile"
                className="w-full h-full object-cover"
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuC8ToM7R5aspM_wjUvPCmYKC9TlN9L3Bdt0XntwKRJuobuPaSeLaUOmrrjRbEXxsKCHyuVVKeQzk4iMW95moxyz6PbGrS5UqUGCldPYGi1xml1yZRZlacNabzOfVKkTRjvwmE67P9-uRqjA-QI85vrOYDXFvRU9C_upHNDmX1EQWiuzVozAdvINrH-gfG5b7ogasdcdupUMhwpk89H1KFN57vuW3tB5lASoBJpyzuw3cXLt0IiM_S7Ds4_6UDFaGNaXmNtyM3xoYRL6"
              />
            </div>
            <div className="flex-1">
              <div className="text-xs font-bold text-on-surface">Alex Chen</div>
              <div className="text-[10px] text-primary">Pro Account</div>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <div className="ml-64 w-full flex flex-col min-h-screen">
        {/* Top Header */}
        <header className="sticky top-0 z-40 flex justify-between items-center px-8 h-16 border-b border-outline-variant/20 bg-surface/80 backdrop-blur-xl">
          <div className="flex items-center gap-8">
            <div className="flex items-center gap-2 bg-surface-container-lowest px-3 py-1.5 rounded-lg border border-outline-variant/10">
              <span className="material-symbols-outlined text-sm text-outline">search</span>
              <input
                className="bg-transparent border-none focus:ring-0 text-xs w-48 text-on-surface placeholder:text-outline-variant uppercase tracking-wider"
                placeholder="Ticker Search"
                type="text"
              />
            </div>
            <div className="flex gap-6">
              <span className="text-primary font-bold border-b border-primary font-body font-medium text-xs uppercase tracking-widest pb-5 mt-5">
                SPY +1.2%
              </span>
              <span className="text-on-surface-variant/50 font-body font-medium text-xs uppercase tracking-widest pb-5 mt-5 hover:text-primary transition-colors cursor-pointer">
                QQQ +0.8%
              </span>
              <span className="text-on-surface-variant/50 font-body font-medium text-xs uppercase tracking-widest pb-5 mt-5 hover:text-primary transition-colors cursor-pointer">
                DIA -0.2%
              </span>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <button className="bg-primary text-on-primary px-4 py-1.5 rounded text-[10px] font-bold uppercase tracking-widest flex items-center gap-2 transition-transform active:scale-95">
              <span className="material-symbols-outlined text-xs">sensors</span>
              Live Feed
            </button>
            <span className="material-symbols-outlined text-on-surface-variant cursor-pointer hover:text-on-surface">
              notifications
            </span>
            <span className="material-symbols-outlined text-on-surface-variant cursor-pointer hover:text-on-surface">
              grid_view
            </span>
          </div>
        </header>

        {/* Main Content Area */}
        <main className="flex-1 p-8">
          {children}
        </main>
      </div>

      {/* Decorative Background */}
      <div className="fixed inset-0 -z-10 pointer-events-none opacity-20">
        <div className="absolute top-[-10%] right-[-5%] w-[40%] h-[40%] bg-primary/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-[-10%] left-[-5%] w-[30%] h-[30%] bg-secondary/5 rounded-full blur-3xl"></div>
      </div>
    </div>
  );
};

export default Layout;
