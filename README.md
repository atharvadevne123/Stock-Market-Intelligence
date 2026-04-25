![Docker](https://github.com/atharvadevne123/Stock-Market-Intelligence/actions/workflows/docker-publish.yml/badge.svg) ![Python Package](https://github.com/atharvadevne123/Stock-Market-Intelligence/actions/workflows/python-publish.yml/badge.svg) ![npm](https://github.com/atharvadevne123/Stock-Market-Intelligence/actions/workflows/npm-publish.yml/badge.svg) ![Bump Version](https://github.com/atharvadevne123/Stock-Market-Intelligence/actions/workflows/bump-version.yml/badge.svg)

# Stock Market Intelligence 📈

A comprehensive **open-source stock market intelligence system** that combines CEO earnings call sentiment analysis, live market news scraping, and technical indicators to generate **BUY/SELL/HOLD signals**.

## Features 🚀

- **📰 Multi-Source News Scraping**: Combines RSS feeds, web scraping, and Reddit for comprehensive market intelligence
- **🧠 FinBERT Sentiment Analysis**: Uses HuggingFace FinBERT for financial sentiment scoring
- **📊 Technical Analysis**: RSI, MACD, Moving Averages, Bollinger Bands, and ATR indicators
- **🎯 Smart Signal Generation**: Combines sentiment + technical analysis for informed trading signals
- **📈 Portfolio Analysis**: Analyze multiple tickers and get portfolio-level recommendations
- **🔄 Real-time Updates**: Scheduled sentiment analysis and signal generation
- **💾 Database Storage**: PostgreSQL for persistent data storage
- **🌐 FastAPI Backend**: RESTful API for integration
- **⚛️ React Frontend**: Modern dashboard for visualization

## Tech Stack

```
Python          | Core backend logic
BeautifulSoup   | Web scraping
feedparser      | RSS feed parsing
PRAW            | Reddit API integration
HuggingFace     | FinBERT sentiment model
yfinance        | Live market data
pandas-ta       | Technical indicators
FastAPI         | REST API framework
PostgreSQL      | Data persistence
React           | Frontend dashboard
Docker          | Containerization
```

## Project Structure

```
Stock Market Intelligence/
├── scraper/                    # News and data scraping modules
│   ├── news_scraper.py        # Multi-source news aggregation
│   ├── reddit_scraper.py      # Reddit sentiment scraping
│   └── earnings_scraper.py    # Earnings call transcripts
│
├── nlp/                        # Natural Language Processing
│   ├── sentiment_analyzer.py  # FinBERT sentiment analysis
│   ├── topic_modeling.py      # LDA topic extraction
│   └── embeddings.py          # Text embeddings
│
├── analysis/                   # Trading Signal Generation
│   ├── signal_engine.py       # BUY/SELL/HOLD signal generator
│   ├── technical_indicators.py # RSI, MACD, Bollinger Bands
│   └── backtester.py          # Strategy backtesting
│
├── api/                        # FastAPI Backend
│   ├── main.py                # API entry point
│   ├── routes/                # API endpoints
│   ├── models.py              # Pydantic data models
│   └── database.py            # Database configuration
│
├── frontend/                   # React Dashboard
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   └── styles/            # CSS styles
│   └── package.json
│
├── database/                   # Database schemas
│   ├── models.py              # SQLAlchemy ORM models
│   ├── migrations/            # Alembic migrations
│   └── schemas.sql            # Initial schema
│
├── scheduler/                  # Task scheduling
│   ├── jobs.py                # Background jobs
│   └── celery_config.py       # Celery configuration
│
├── docker/                     # Docker configuration
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── tests/                      # Unit and integration tests
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## Installation 🔧

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Node.js 16+
- Docker & Docker Compose (optional)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/stock-market-intelligence.git
cd "Stock Market Intelligence"
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Upgrade pip
python3 -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

#### Required Environment Variables:
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/stock_intelligence

# API Keys
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_SECRET=your_reddit_secret
NEWS_API_KEY=your_newsapi_key

# System
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### 4. Set Up PostgreSQL Database

```bash
# Create database
createdb stock_intelligence

# Run migrations (Alembic)
alembic upgrade head
```

### 5. Run the Modules

```bash
# Test news scraper
python scraper/news_scraper.py

# Test sentiment analyzer
python nlp/sentiment_analyzer.py

# Test signal engine
python analysis/signal_engine.py

# Run orchestrator
python main_orchestrator.py
```

## Usage 📚

### Single Ticker Analysis

```python
from main_orchestrator import StockMarketIntelligence

# Initialize system
system = StockMarketIntelligence()

# Analyze single ticker
analysis = system.analyze_ticker("AAPL", hours=24)

print(f"Signal: {analysis['signal']['final_signal']}")
print(f"Confidence: {analysis['signal']['combined_score']}")
```

### Portfolio Analysis

```python
# Analyze multiple tickers
portfolio = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
portfolio_analysis = system.analyze_portfolio(portfolio)

print(f"Recommendation: {portfolio_analysis['summary']['recommendation']}")
print(f"Signals: {portfolio_analysis['summary']['signal_distribution']}")
```

### Market Overview

```python
# Get overall market sentiment
market = system.get_market_overview(hours=24)

print(f"Market Trend: {market['market_trend']}")
print(f"Sentiment Ratio: {market['sentiment_ratios']}")
```

### API Usage (FastAPI)

```bash
# Start API server
python api/main.py

# API endpoints
GET /api/analyze/{ticker}           # Analyze single ticker
GET /api/portfolio?tickers=AAPL,MSFT  # Analyze portfolio
GET /api/market/overview            # Market overview
GET /api/signals/history?ticker=AAPL # Signal history
POST /api/alerts/subscribe          # Subscribe to alerts
```

## Features in Detail 🔍

### 1. News Aggregation 📰

**Sources:**
- CNN Money
- Reuters
- Bloomberg
- Seeking Alpha
- MarketWatch
- Yahoo Finance
- Reddit r/stocks

**Capabilities:**
- Real-time RSS feed scraping
- Web scraping with BeautifulSoup
- Reddit sentiment collection via PRAW
- Ticker-specific news filtering
- Time-based news filtering

### 2. Sentiment Analysis 🧠

**Model:** ProsusAI/finbert (FinBERT)

**Features:**
- Financial-specific sentiment classification
- Batch processing support
- Confidence scoring
- Article-level and batch aggregation
- GPU acceleration support

**Output:**
```json
{
  "sentiment": "positive",
  "confidence": 0.92,
  "scores": {
    "positive": 0.92,
    "negative": 0.03,
    "neutral": 0.05
  }
}
```

### 3. Technical Analysis 📊

**Indicators:**
- **RSI** (Relative Strength Index) - Momentum
- **MACD** (Moving Average Convergence Divergence) - Trend
- **Bollinger Bands** - Volatility
- **Moving Averages** (50-day, 200-day) - Trend
- **ATR** (Average True Range) - Risk

**Signal Logic:**
- RSI > 70 → SELL, RSI < 30 → BUY
- MACD crossover → BUY/SELL signals
- Price outside Bollinger Bands → Reversal signals
- Moving average crossover → Trend signals

### 4. Signal Generation 🎯

**Signal Types:**
- `STRONG_BUY` - 3-4 indicators agree
- `BUY` - 2 indicators agree
- `HOLD` - Mixed signals
- `SELL` - 2 indicators agree
- `STRONG_SELL` - 3-4 indicators agree

**Weighting:**
- Technical Analysis: 70%
- Sentiment Analysis: 30%

## Examples 💡

### Example 1: Quick Single Stock Analysis

```python
from main_orchestrator import StockMarketIntelligence

system = StockMarketIntelligence()
analysis = system.analyze_ticker("NVDA")

# Results
print(f"Ticker: {analysis['ticker']}")
print(f"Signal: {analysis['signal']['final_signal']}")
print(f"Latest Price: ${analysis['signal']['technical']['latest_price']}")
print(f"Price Change: {analysis['signal']['technical']['price_change_percent']}%")
```

### Example 2: Sentiment Tracking

```python
from nlp.sentiment_analyzer import NewsArticleSentimentAnalyzer

analyzer = NewsArticleSentimentAnalyzer()

result = analyzer.analyze_article(
    title="Apple Beats Earnings, Stock Surges",
    content="Apple reported Q4 revenue of $89.5B..."
)

print(f"Title Sentiment: {result['title_sentiment']['sentiment']}")
print(f"Content Sentiment: {result['content_sentiment']['sentiment']}")
print(f"Combined: {result['combined_sentiment']}")
```

### Example 3: Technical Indicator Analysis

```python
from analysis.signal_engine import TechnicalSignalGenerator

gen = TechnicalSignalGenerator()
signal = gen.generate_technical_signal("MSFT")

print(f"Signal: {signal['signal']}")
print(f"RSI: {signal['technical_data']['rsi']}")
print(f"Individual Signals: {signal['individual_signals']}")
```

## Database Schema 💾

### Articles Table
```sql
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10),
    title VARCHAR(500),
    content TEXT,
    source VARCHAR(100),
    url VARCHAR(500),
    published_date TIMESTAMP,
    sentiment VARCHAR(20),
    sentiment_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Signals Table
```sql
CREATE TABLE signals (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10),
    signal VARCHAR(20),
    confidence FLOAT,
    technical_score FLOAT,
    sentiment_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## API Endpoints 🔌

```
Market Data:
  GET  /api/market/overview
  GET  /api/market/news?ticker=AAPL&hours=24

Signals:
  GET  /api/signals/{ticker}
  GET  /api/signals/portfolio?tickers=AAPL,MSFT
  GET  /api/signals/history?ticker=AAPL&days=30

Sentiment:
  GET  /api/sentiment/{ticker}
  GET  /api/sentiment/batch?tickers=AAPL,MSFT

Technical:
  GET  /api/technical/{ticker}
  GET  /api/technical/indicators?ticker=AAPL

Admin:
  POST /api/admin/refresh?ticker=AAPL
  GET  /api/admin/status
```

## Performance 🚀

- **News Scraping**: 10-15 sources/sec
- **Sentiment Analysis**: 5-10 articles/sec (GPU), 1-2 articles/sec (CPU)
- **Signal Generation**: <1 second per ticker
- **Portfolio Analysis**: <30 seconds for 100 tickers

## Backtesting 📉

Test your strategy against historical data:

```python
from analysis.backtester import BacktestEngine

backtest = BacktestEngine()
results = backtest.run(
    ticker="AAPL",
    strategy="comprehensive_signals",
    start_date="2022-01-01",
    end_date="2024-01-01"
)

print(f"Total Return: {results['total_return']:.2%}")
print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
print(f"Win Rate: {results['win_rate']:.1%}")
```

## Deployment 🐳

### Docker Setup

```bash
# Build Docker image
docker build -f docker/Dockerfile -t stock-intel .

# Run with Docker Compose
docker-compose -f docker/docker-compose.yml up

# Access services
API: http://localhost:8000
Frontend: http://localhost:3000
```

### Cloud Deployment

```bash
# Deploy to AWS (example)
aws ecr get-login-password --region us-east-1 | docker login ...
docker tag stock-intel:latest <AWS_ECR_URI>/stock-intel:latest
docker push <AWS_ECR_URI>/stock-intel:latest
```

## Testing 🧪

```bash
# Run unit tests
pytest tests/

# Run with coverage
pytest --cov=scraper tests/

# Integration tests
pytest tests/integration/
```

## Troubleshooting 🔧

### FinBERT Model Download Issues
```bash
# Pre-download model
python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; \
AutoTokenizer.from_pretrained('ProsusAI/finbert'); \
AutoModelForSequenceClassification.from_pretrained('ProsusAI/finbert')"
```

### Database Connection Errors
```bash
# Test PostgreSQL connection
psql -h localhost -U user -d stock_intelligence -c "SELECT 1"

# Check DATABASE_URL in .env
echo $DATABASE_URL
```

### CUDA/GPU Issues
```bash
# Check if CUDA is available
python -c "import torch; print(torch.cuda.is_available())"

# Force CPU mode
export DEVICE=cpu
```

## Contributing 🤝

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## Disclaimer ⚠️

This tool is for **educational purposes only**. It is NOT financial advice. Always:
- Do your own research (DYOR)
- Consult with a financial advisor
- Never invest more than you can afford to lose
- Backtest strategies before live trading

## License 📄

MIT License - See LICENSE.txt for details

## Roadmap 🗺️

- [ ] Real-time streaming with WebSockets
- [ ] Advanced hedging strategies
- [ ] Options analysis module
- [ ] Multi-timeframe analysis
- [ ] Community signal sharing
- [ ] Mobile app (iOS/Android)
- [ ] AI model fine-tuning on custom data
- [ ] Alternative data integration (satellite imagery, credit card data)

## Acknowledgments 🙏

- HuggingFace for FinBERT model
- yfinance for market data
- Beautiful Soup community
- FastAPI framework
- React ecosystem

---

**Happy trading! 🚀 Remember: Past performance is not indicative of future results.**