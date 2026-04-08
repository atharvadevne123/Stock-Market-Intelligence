# 🚀 Quick Start Guide - Stock Market Intelligence Dashboard

Get the fully functional website up and running in 5 minutes!

## Prerequisites
- Node.js 16+ ([Download](https://nodejs.org/))
- npm (comes with Node.js)
- Git

## ⚡ Quick Start (5 Minutes)

### Step 1: Install Dependencies
```bash
cd frontend
npm install
```
⏱️ **Duration**: 2-3 minutes (depending on internet speed)

### Step 2: Start Development Server
```bash
npm start
```

The website will automatically open at: **http://localhost:3000**

### Step 3: Explore the Dashboard!

You should now see the "Sovereign Terminal" dashboard with:

| Page | URL | Features |
|------|-----|----------|
| 📊 **Dashboard** | http://localhost:3000/ | Market overview, top signals, intelligence feed |
| 📈 **NVDA Analysis** | http://localhost:3000/ticker/nvda | Detailed ticker analysis with technical indicators |
| 💼 **Portfolio** | http://localhost:3000/portfolio | Portfolio tracking with backtest metrics |
| 🗺️ **Market Map** | http://localhost:3000/market | Sector performance and trends |
| 🔔 **Signals** | http://localhost:3000/signals | Real-time intelligence feed with sentiment analysis |

## 🎮 How to Use the Dashboard

### Dashboard (Home Page)
1. View **Market Pulse Index** - shows overall market sentiment
2. Check **Top Signals** - NVDA, TSLA, AMD, AAPL stocks with buy/sell signals
3. Monitor **Intelligence Feed** - real-time news sentiment

### NVDA Ticker Page
1. See **Strong Buy Signal** with 92% confidence
2. View **Technical Chart** with different timeframes (1H, 4H, 1D, 1W)
3. Check **Technical Indicators** - RSI, MACD, Bollinger Bands
4. Read **Sentiment Analysis** - FinBERT scores from multiple sources
5. Review **Earnings Intelligence** - CEO confidence and key phrases
6. **Trade** - Click "Open Long Trade" or "Short Position" buttons

### Portfolio Page
1. See **Portfolio Outlook** - currently showing "Bullish"
2. Check **Backtest History** - 84.2% accuracy, +12.4% profitability
3. View **Tracked Tickers Table** - AAPL, MSFT, TSLA, NVDA with:
   - Current price
   - 24h change
   - Sentiment score
   - Technical signal
   - Buy/Sell recommendation
4. Monitor **Sharpe Ratio** (3.24 - High Efficiency)

### Market Map
1. View **Market Sentiment** - 84.2 EXTREME GREED
2. See **Sentiment Breakdown**:
   - 68% Positive
   - 14% Neutral
   - 18% Negative
3. Check **Sector Performance** - Tech, Healthcare, Finance, etc.

### Signals Page
1. Filter signals by **Ticker** (TSLA, NVDA, BTC, AAPL)
2. Set **Sentiment Threshold** (Highly Positive, Neutral, Negative)
3. Toggle **Data Sources** (Reddit, Bloomberg, Reuters)
4. View **Intelligence Cards** with:
   - FinBERT sentiment scores
   - Source and timestamp
   - Full article headline
   - Relevant tags
5. Monitor **Sentiment Divergence** - Social vs Institutional
6. Check **FinBERT Latency** - Processing speed

## 🎨 What You'll See

### Professional Design Features
- ✅ **Dark Theme** - Easy on the eyes, professional look
- ✅ **Smooth Animations** - Glowing indicators, transitions
- ✅ **Responsive Layouts** - Works on desktop, tablet, mobile
- ✅ **Real Data** - Demo data included, ready for API integration
- ✅ **Professional Icons** - Material Design Symbols

### Key Components
- **Bento Grid Layouts** - Modern, organized sections
- **Signal Indicators** - Color-coded (green = buy, red = sell)
- **Progress Bars** - Sentiment levels with visual indicators
- **Technical Charts** - SVG price charts with trend lines
- **Data Tables** - Comprehensive ticker information
- **Feed Cards** - News items with sentiment badges

## 📊 Understanding the Signals

### Buy Signal (🟢 Green)
- Indicates strong bullish sentiment
- Shown in primary color (#4edea3)
- Example: NVDA with STRONG BUY signal

### Sell Signal (🔴 Red)
- Indicates bearish sentiment
- Shown in secondary color (#ffb2b7)
- Example: TSLA with STRONG SELL signal

### Neutral/Hold (🟠 Orange)
- Indicates caution or consolidation
- Shown in tertiary color (#ffb95f)
- Example: AAPL with WATCH signal

## 🔧 Development Features

### Hot Reload
Changes to files auto-reload in the browser. Just edit and save!

### React Developer Tools
- Install [React DevTools](https://chrome.google.com/webstore/detail/react-developer-tools/) browser extension
- Inspect component props and state
- Time travel debugging

### Responsive Design Testing
- Open DevTools (F12 or Cmd+Option+I)
- Click device emulation (tablet/mobile icons)
- Test on different screen sizes

## 📦 Build for Production

When ready to deploy:

```bash
npm run build
```

This creates an optimized `build/` folder ready for deployment to:
- Vercel
- Netlify
- AWS S3
- Any static hosting provider

## 🚨 Common Issues & Solutions

### "Port 3000 already in use"
Use a different port:
```bash
PORT=3001 npm start
```

### "npm command not found"
Node.js/npm not installed:
1. [Download Node.js](https://nodejs.org/)
2. Restart terminal
3. Try again

### "Module not found" error
Reinstall dependencies:
```bash
rm -rf node_modules
npm install
npm start
```

### Styles not loading
Clear browser cache:
- Ctrl+Shift+R (Windows)
- Cmd+Shift+R (Mac)

## 🔌 Next Steps: Integrate with Backend

When your backend API is running:

1. **Update API endpoints** in page components:
   ```javascript
   // In MarketPage.js, PortfolioPage.js, etc.
   const response = await axios.get('http://your-api.com/endpoint');
   ```

2. **Set environment variables**:
   Create `.env` file in `frontend/`:
   ```
   REACT_APP_API_URL=http://localhost:8000
   REACT_APP_API_KEY=your_key_here
   ```

3. **Use in components**:
   ```javascript
   const apiUrl = process.env.REACT_APP_API_URL;
   ```

## 📚 Documentation

- **Full Guide**: See `UI_IMPLEMENTATION_GUIDE.md`
- **Frontend README**: See `frontend/README.md`
- **React Docs**: https://react.dev
- **Tailwind Docs**: https://tailwindcss.com

## ✨ Features Overview

### Dashboard Features
- Real-time market pulse
- Top stock signals
- Intelligence feed
- Sector heatmap
- Live feed status

### Ticker Analysis
- Master signal indicator (92% confidence)
- Price charts with technical indicators
- FinBERT sentiment analysis
- News from multiple sources
- Earnings intelligence
- CEO confidence metrics

### Portfolio Management
- Portfolio outlook (Bullish/Bearish)
- Backtest history
- Signal accuracy metrics
- Comprehensive ticker table
- Sharpe ratio display

### Market Intelligence
- Market-wide sentiment
- Sector performance
- Volatility tracking
- Trend analysis

### Signal Intelligence
- Real-time signal feed
- Sentiment filtering
- Source selection
- Divergence tracking
- Processing latency monitoring

## 🎯 Tips for Best Experience

1. **Use Chrome/Edge** - Best compatibility and DevTools
2. **Full Screen** - Maximize dashboard view
3. **Enable JavaScript** - Dashboard requires JS
4. **Clear Cache** - If styles look off
5. **Responsive Mode** - Test on different sizes

## 🚀 You're Ready!

The Stock Market Intelligence Dashboard is now running on your machine!

### What's Next?
1. ✅ Explore all pages
2. ✅ Check different tickers
3. ✅ Review portfolio analysis
4. ✅ Monitor signals
5. ✅ Connect to your backend API

## 💡 Pro Tips

- **Navigate quickly**: Use the sidebar menu
- **Search tickers**: Use the search bar at top
- **Check live feeds**: Intelligence section updates in real-time
- **Monitor signals**: Color-coded indicators show sentiment at a glance
- **Export data**: Use the Export button in dashboard

## 🆘 Need Help?

1. Check the `UI_IMPLEMENTATION_GUIDE.md` for detailed documentation
2. Review `frontend/README.md` for technical details
3. Check browser console for error messages (F12)
4. Make sure Node.js and npm are installed

## 🎉 Success!

Your Stock Market Intelligence Dashboard is now running!

**Remember**: This is a demo with sample data. Connect it to your backend API to get real market data!

---

**Happy Trading! 📈**
