# Stock Market Intelligence - Frontend

## 🚀 Sovereign Terminal UI

A fully functional, responsive stock market analysis dashboard built with React, Tailwind CSS, and Material Design icons.

### Features

#### 📊 Dashboard (Market Overview)
- **Market Pulse Index**: Real-time market sentiment analysis with fear/greed indicator
- **Top Signals**: Live stock signals with buy/sell recommendations
- **Technical Heatmap**: Sector-by-sector performance tracking
- **Intelligence Feed**: Real-time news sentiment analysis using FinBERT

#### 📈 Ticker Analysis (NVDA Example)
- **Master Signal Indicator**: Comprehensive buy/sell signals with confidence scores
- **Technical Chart**: Interactive price charts with RSI, MACD, and Bollinger Bands
- **FinBERT Neural Sentiment**: AI-powered sentiment analysis from multiple sources
- **Earnings Intelligence**: CEO confidence metrics and key phrase extraction
- **Trade Actions**: Quick access to open long/short positions

#### 💼 Portfolio Analysis
- **Executive Summary**: Portfolio outlook (Bullish/Bearish/Neutral)
- **Backtest History**: 30-day signal accuracy and profitability metrics
- **Tracked Tickers Table**: Comprehensive portfolio with sentiment scores and recommendations
- **Sharpe Ratio Display**: Real-time risk-adjusted return metrics

#### 📡 Market Map
- **Sector Performance**: All major sectors with sentiment indicators
- **Market Metrics**: Articles analyzed and engine latency
- **Trend Analysis**: Market momentum and volatility tracking

#### 🔔 Signals & Intelligence Feed
- **Real-time Sentiment Analysis**: FinBERT-powered news categorization
- **Smart Filters**: Filter by ticker, sentiment threshold, and data source
- **Live Scraping Engine**: 15.8+ sources per second analysis
- **Sentiment Divergence Tracking**: Social vs. institutional sentiment comparison

### 🎨 Design System

**Color Palette:**
- Primary: #4edea3 (Teal/Green)
- Secondary: #ffb2b7 (Red/Pink - for bearish signals)
- Tertiary: #ffb95f (Orange - for neutral/caution)
- Background: #0b1326 (Deep Navy)

**Typography:**
- Headline: Manrope (bold, large headlines)
- Body: Inter (readable, regular text)
- Label: Inter (small labels and tags)

**Components:**
- Bento grid layouts
- Glass-morphism effects
- Glowing signal indicators
- Animated progress bars
- Material Design icons

### 📦 Installation

```bash
cd frontend
npm install
```

### 🏃 Running the Development Server

```bash
npm start
```

The app will open at `http://localhost:3000`

### 🏗️ Build for Production

```bash
npm run build
```

Creates an optimized production build in the `build/` directory.

### 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── Layout.js           # Shared layout with sidebar and header
│   ├── pages/
│   │   ├── DashboardPage.js    # Market overview dashboard
│   │   ├── TickerPage.js       # Individual ticker analysis (NVDA)
│   │   ├── PortfolioPage.js    # Portfolio tracking
│   │   ├── MarketPage.js       # Market map and sectors
│   │   └── SignalsPage.js      # Intelligence feed and signals
│   ├── App.js                  # Main router configuration
│   ├── index.js                # React entry point
│   └── index.css               # Global Tailwind styles
├── public/
│   └── index.html              # HTML template
├── tailwind.config.js          # Tailwind configuration
├── postcss.config.js           # PostCSS configuration
└── package.json                # Dependencies
```

### 🔌 API Integration Points

The frontend is designed to work with the backend API:

**Endpoints Used:**
- `GET /api/market/overview` - Market overview data
- `GET /api/ticker/{symbol}` - Individual ticker analysis
- `GET /api/portfolio` - Portfolio data
- `GET /api/signals` - Real-time signals

### 🎯 Key Pages

| Page | Route | Purpose |
|------|-------|---------|
| Dashboard | `/` | Market overview and top signals |
| NVDA Analysis | `/ticker/nvda` | Detailed ticker analysis |
| Portfolio | `/portfolio` | Portfolio tracking and analysis |
| Market Map | `/market` | Sector performance and trends |
| Signals | `/signals` | Intelligence feed and sentiment analysis |

### 🛠️ Technologies Used

- **React 18.2**: UI framework
- **React Router 6**: Navigation
- **Tailwind CSS 3.3**: Styling framework
- **PostCSS**: CSS processing
- **Axios**: HTTP client (for API calls)
- **Material Symbols**: Icon library
- **Google Fonts**: Typography

### 📱 Responsive Design

- Fully responsive from mobile to desktop
- Tailwind breakpoints: sm, md, lg, xl
- Adaptive layouts using CSS Grid and Flexbox
- Touch-friendly UI elements

### ✨ Features Highlights

1. **Real-time Updates**: WebSocket support ready for live data
2. **Dark Mode**: Built-in dark theme following Material Design 3
3. **Performance**: Optimized renders and lazy loading
4. **Accessibility**: ARIA labels and keyboard navigation
5. **Mobile Friendly**: Responsive design works on all devices

### 🔐 Security

- No sensitive data stored in frontend
- API calls use HTTPS in production
- CORS headers properly configured
- Input validation on all forms

### 📊 Data Visualization

- Responsive SVG charts
- CSS animations for smooth transitions
- Gradient overlays and blur effects
- Live counter animations

### 🚀 Deployment

The frontend can be deployed to:
- Vercel (recommended)
- Netlify
- AWS S3 + CloudFront
- GitHub Pages
- Any static hosting service

### 📚 Dependencies

```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-router-dom": "^6.17.0",
  "axios": "^1.6.0",
  "tailwindcss": "^3.3.6",
  "postcss": "^8.4.31",
  "autoprefixer": "^10.4.16"
}
```

### 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test on multiple browsers
4. Submit a pull request

### 📄 License

MIT License - See LICENSE file for details

### 📞 Support

For issues or questions:
1. Check existing GitHub issues
2. Create a new issue with details
3. Contact the development team

---

**Built with ❤️ by the Stock Market Intelligence Team**
