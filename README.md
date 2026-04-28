![Docker](https://github.com/atharvadevne123/Stock-Market-Intelligence/actions/workflows/docker-publish.yml/badge.svg) ![Python Package](https://github.com/atharvadevne123/Stock-Market-Intelligence/actions/workflows/python-publish.yml/badge.svg) ![npm](https://github.com/atharvadevne123/Stock-Market-Intelligence/actions/workflows/npm-publish.yml/badge.svg) ![Bump Version](https://github.com/atharvadevne123/Stock-Market-Intelligence/actions/workflows/bump-version.yml/badge.svg)

# Stock Market Intelligence — Sovereign Terminal

A full-stack stock market intelligence platform that combines **FinBERT sentiment analysis**, **technical indicators**, and a **geopolitical tension index (GTI)** to generate BUY/SELL/HOLD trading signals — visualised through a real-time 3D intelligence terminal.

---

## Screenshots

### Earth Pulse — Live Geopolitical Globe
![Globe](screenshots/globe.png)

### Geo Map — Regional Tension Heatmap
![Geo Map](screenshots/map.png)

### AI Signals — Trading Recommendations
![AI Signals](screenshots/signals.png)

### AI Signals — Expanded Reasoning Chain
![AI Signals Expanded](screenshots/signals_expanded.png)

### Portfolio — Holdings & GTI Risk Overlay
![Portfolio](screenshots/portfolio.png)

### Scenario Simulator — Impact Forecasting
![Simulation](screenshots/simulation.png)

---

## How It Works

```
News & Events  ──►  FinBERT Sentiment Analyzer
GDELT / Reddit ──►  Transformer Event Classifier
yfinance       ──►  Technical Indicators (RSI, MACD, Bollinger Bands)
                            │
                            ▼
               Geopolitical Tension Index (GTI)
               Weighted 0–100 per country / region
                            │
                            ▼
               LightGBM Model
               ──► BUY / SELL / HOLD + Confidence %
                            │
                            ▼
               Sovereign Terminal UI
               Globe · Geo Map · Signal Cards · Portfolio
```

---

## Features

### Intelligence Pipeline
- **FinBERT Sentiment Analysis** — financial-domain NLP model scores news articles positive / negative / neutral
- **Transformer Event Classifier** — classifies events into military escalation, trade restrictions, sanctions, diplomatic activity
- **Technical Indicators** — RSI, MACD, Bollinger Bands, Moving Averages (50/200-day), ATR
- **LightGBM Signal Model** — combines sentiment score (30%) + technical score (70%) → final signal with confidence %
- **Geopolitical Tension Index** — custom weighted score aggregating conflict severity, regional spread, and economic exposure per country

### Frontend (Sovereign Terminal)
- **Earth Pulse** — 3D globe with country polygons coloured by GTI score, animated conflict arcs, live event markers, auto-rotation, click-to-focus country panel
- **Geo Map** — Mercator world map with real country polygons (react-simple-maps), tension colour fill, zoom/pan, region breakdown sidebar
- **AI Signals** — trading signal cards for each instrument showing confidence bar, 3-step AI reasoning chain (event → macro narrative → market impact), NLP stats, 48h GTI history chart
- **Portfolio** — holdings table sortable by GTI risk / P&L / value, risk meter gauge, asset class breakdown, geopolitical alert list
- **Scenario Simulator** — adjust Oil Shock, Rate Change, Escalation, Supply Chain, Cyber Threat sliders → computes adjusted GTI and per-asset price impact forecasts in real time

---

## Tech Stack

| Layer | Technology |
|---|---|
| Sentiment Analysis | FinBERT (`ProsusAI/finbert`) |
| Event Classification | Transformer (HuggingFace) |
| Signal Model | LightGBM |
| Technical Indicators | pandas-ta (RSI, MACD, BB, ATR) |
| Market Data | yfinance |
| News Scraping | BeautifulSoup · feedparser · PRAW (Reddit) |
| Backend API | FastAPI |
| Database | PostgreSQL + SQLAlchemy + Alembic |
| Task Scheduler | Celery |
| Frontend Framework | React 18 + Vite |
| Styling | Tailwind CSS |
| 3D Globe | react-globe.gl (Three.js) |
| World Map | react-simple-maps |
| State Management | Zustand |
| Charts | Recharts |
| Animations | Framer Motion |

---

## Project Structure

```
Stock Market Intelligence/
├── scraper/                       # Data collection
│   ├── news_scraper.py            # Multi-source news (RSS, web, Reddit)
│   ├── reddit_scraper.py          # Reddit sentiment via PRAW
│   └── earnings_scraper.py        # Earnings call transcripts
│
├── nlp/                           # NLP pipeline
│   ├── sentiment_analyzer.py      # FinBERT scoring
│   ├── topic_modeling.py          # Macro narrative extraction (LDA)
│   └── embeddings.py              # Text embeddings
│
├── analysis/                      # Signal generation
│   ├── signal_engine.py           # LightGBM BUY/SELL/HOLD model
│   ├── technical_indicators.py    # RSI, MACD, Bollinger Bands, ATR
│   └── backtester.py              # Historical strategy backtesting
│
├── api/                           # FastAPI backend
│   ├── main.py
│   ├── routes/
│   ├── models.py
│   └── database.py
│
├── frontend/                      # Sovereign Terminal UI
│   ├── src/
│   │   ├── components/
│   │   │   ├── globe/             # 3D globe (react-globe.gl)
│   │   │   ├── map/               # Geo map (react-simple-maps)
│   │   │   ├── signals/           # AI signal cards + reasoning chains
│   │   │   └── portfolio/         # Holdings & risk view
│   │   ├── data/
│   │   │   ├── globe.js           # GTI country data, conflict arcs, events
│   │   │   └── signals.js         # Trading signals, NLP stats, GTI history
│   │   ├── store.js               # Zustand state + simulation engine
│   │   └── App.jsx
│   ├── index.html
│   └── vite.config.js
│
├── database/                      # DB schemas + migrations
├── scheduler/                     # Celery background jobs
├── docker/                        # Dockerfile + docker-compose
├── screenshots/                   # UI screenshots
├── tests/
├── requirements.txt
└── .env.example
```

---

## Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Node.js 18+

### 1. Clone & set up Python

```bash
git clone https://github.com/atharvadevne123/Stock-Market-Intelligence.git
cd "Stock Market Intelligence"

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

```env
DATABASE_URL=postgresql://user:password@localhost:5432/stock_intelligence
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_SECRET=your_reddit_secret
NEWS_API_KEY=your_newsapi_key
ENVIRONMENT=development
```

### 3. Set up database

```bash
createdb stock_intelligence
alembic upgrade head
```

### 4. Run the backend

```bash
python api/main.py          # FastAPI → http://localhost:8000
# or run the full pipeline:
python main_orchestrator.py
```

### 5. Run the frontend

```bash
cd frontend
npm install
npm run dev                  # → http://localhost:3000
```

---

## API Reference

```
GET  /api/signals/{ticker}              BUY/SELL/HOLD + confidence %
GET  /api/signals/portfolio             Multi-ticker portfolio analysis
GET  /api/sentiment/{ticker}            FinBERT sentiment score
GET  /api/technical/{ticker}            RSI, MACD, Bollinger Bands, ATR
GET  /api/market/overview               Global market sentiment summary
GET  /api/gti/{country}                 Geopolitical Tension Index score
POST /api/admin/refresh?ticker=AAPL     Trigger fresh data pull
```

---

## Signal Logic

**Weights:** Technical Analysis 70% · Sentiment 30%

| Signal | Condition |
|---|---|
| STRONG_BUY | 3–4 indicators agree bullish + positive sentiment |
| BUY | 2 indicators agree bullish |
| HOLD | Mixed / insufficient signal strength |
| SELL | 2 indicators agree bearish |
| STRONG_SELL | 3–4 indicators agree bearish + negative sentiment |

GTI > 65 → risk premium expansion → equity SELL pressure applied
GTI > 80 in commodity region → supply shock → commodity BUY bias applied

---

## Scenario Simulator

| Slider | Effect |
|---|---|
| Oil Price Shock | Increases oil/energy prices, pressures equities, weakens USD |
| Interest Rate Change | Strengthens USD, depresses bonds and growth equities |
| Geopolitical Escalation | Raises GTI, boosts gold/oil safe-haven demand, sells equities |
| Supply Chain Disruption | Pressures tech/manufacturing, lifts agricultural commodities |
| Cyber Threat Level | Adds volatility to financials and tech sector |

Output: adjusted GTI score, per-asset price impact %, BUY/SELL/HOLD signals, threshold alerts.

---

## Disclaimer

For **educational purposes only**. Not financial advice. Always do your own research and consult a qualified financial advisor before trading.

---

## License

MIT License
