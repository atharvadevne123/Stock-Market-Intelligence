# Stock Market Intelligence API Documentation

## Quick Start

### 1. Start the API Server

```bash
cd "/Users/atharvadevne/Python/Stock Market Intelligence"
source venv/bin/activate
python api/main.py
```

The API will be available at: **http://localhost:8000**

### 2. Access Interactive Documentation

- **Swagger UI (Interactive)**: http://localhost:8000/docs
- **ReDoc (Alternative UI)**: http://localhost:8000/redoc

### 3. Test an Endpoint

```bash
curl http://localhost:8000/api/analyze/AAPL
```

---

## API Endpoints Overview

### Health & Status
- `GET /` - API info
- `GET /health` - Health check
- `GET /status` - System status

### Analysis
- `GET /api/analyze/{ticker}` - Analyze single ticker
- `POST /api/analyze/batch` - Analyze multiple tickers
- `GET /api/portfolio` - Analyze portfolio (query string)

### News
- `GET /api/news/market` - Get market news
- `GET /api/news/{ticker}` - Get ticker-specific news
- `GET /api/news/search` - Search for news

### Sentiment
- `POST /api/sentiment/analyze` - Analyze article sentiment
- `GET /api/sentiment/{ticker}` - Get aggregated sentiment

### Signals
- `GET /api/signals/{ticker}` - Get trading signal
- `POST /api/signals/batch` - Get signals for multiple tickers

### Technical
- `GET /api/technical/{ticker}` - Get technical analysis

### Market
- `GET /api/market/overview` - Get market overview

### Utility
- `GET /api/tickers/popular` - Get popular tickers
- `GET /api/signals/interpretation` - Signal explanations

---

## Detailed Endpoint Documentation

### GET /api/analyze/{ticker}
**Comprehensive analysis for a single stock**

#### Parameters
- `ticker` (path, required): Stock ticker symbol (e.g., "AAPL")
- `hours` (query, optional): Hours of news to analyze (default: 24)

#### Example Request
```bash
curl http://localhost:8000/api/analyze/AAPL?hours=24
```

#### Example Response
```json
{
  "ticker": "AAPL",
  "timestamp": "2026-03-06T13:30:00",
  "news": {
    "articles_found": 15,
    "articles": [
      {
        "title": "Apple Stock Surges",
        "source": "reuters",
        "url": "https://...",
        "published_date": "2026-03-06T12:00:00"
      }
    ]
  },
  "sentiment": {
    "articles_analyzed": 10,
    "results": [
      {
        "combined_sentiment": "positive",
        "combined_confidence": 0.85
      }
    ]
  },
  "signal": {
    "ticker": "AAPL",
    "final_signal": "BUY",
    "combined_score": 0.654,
    "confidence": 0.75,
    "technical": {
      "signal": "BUY",
      "latest_price": 150.25,
      "price_change_percent": 2.5
    },
    "sentiment": {
      "signal": "BUY",
      "articles_analyzed": 10
    }
  }
}
```

---

### POST /api/analyze/batch
**Analyze multiple tickers**

#### Request Body
```json
{
  "tickers": ["AAPL", "MSFT", "GOOGL"],
  "hours": 24
}
```

#### Example cURL
```bash
curl -X POST http://localhost:8000/api/analyze/batch \
  -H "Content-Type: application/json" \
  -d '{
    "tickers": ["AAPL", "MSFT", "GOOGL"],
    "hours": 24
  }'
```

#### Response
```json
{
  "portfolio": ["AAPL", "MSFT", "GOOGL"],
  "timestamp": "2026-03-06T13:30:00",
  "analyses": [
    {
      "ticker": "AAPL",
      "signal": { ... }
    }
  ],
  "summary": {
    "total_analyzed": 3,
    "signal_distribution": {
      "STRONG_BUY": 1,
      "BUY": 1,
      "HOLD": 1,
      "SELL": 0,
      "STRONG_SELL": 0
    },
    "recommendation": "BULLISH"
  }
}
```

---

### GET /api/portfolio
**Portfolio analysis with query string**

#### Parameters
- `tickers` (query, required): Comma-separated tickers (e.g., "AAPL,MSFT,GOOGL")
- `hours` (query, optional): Hours to analyze (default: 24)

#### Example Request
```bash
curl "http://localhost:8000/api/portfolio?tickers=AAPL,MSFT,GOOGL&hours=24"
```

---

### GET /api/news/{ticker}
**Get ticker-specific news**

#### Parameters
- `ticker` (path, required): Stock ticker
- `hours` (query, optional): Hours to look back

#### Example Request
```bash
curl "http://localhost:8000/api/news/AAPL?hours=48"
```

#### Response
```json
{
  "ticker": "AAPL",
  "articles_found": 12,
  "articles": [
    {
      "title": "Apple Q4 Earnings Beat",
      "content": "Apple reported strong Q4 results...",
      "source": "cnbc",
      "url": "https://...",
      "published_date": "2026-03-06T11:30:00",
      "ticker": "AAPL"
    }
  ]
}
```

---

### POST /api/sentiment/analyze
**Analyze sentiment of an article**

#### Request Body
```json
{
  "title": "Apple Beats Earnings Expectations",
  "content": "Apple reported strong Q4 results with revenue of $89.5B, exceeding analyst expectations..."
}
```

#### Example cURL
```bash
curl -X POST http://localhost:8000/api/sentiment/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Apple Beats Earnings",
    "content": "Strong Q4 results"
  }'
```

#### Response
```json
{
  "title_sentiment": {
    "sentiment": "neutral",
    "confidence": 0.82
  },
  "content_sentiment": {
    "sentiment": "positive",
    "confidence": 0.95
  },
  "combined_sentiment": "positive",
  "combined_confidence": 0.88,
  "all_scores": {
    "positive": 0.55,
    "negative": 0.02,
    "neutral": 0.43
  }
}
```

---

### GET /api/sentiment/{ticker}
**Get aggregated sentiment for a ticker**

#### Parameters
- `ticker` (path, required): Stock ticker
- `hours` (query, optional): Hours to analyze

#### Example Request
```bash
curl "http://localhost:8000/api/sentiment/AAPL?hours=24"
```

#### Response
```json
{
  "ticker": "AAPL",
  "articles_analyzed": 10,
  "sentiment_distribution": {
    "positive": 6,
    "negative": 1,
    "neutral": 3
  },
  "sentiment_ratios": {
    "positive": 0.6,
    "negative": 0.1,
    "neutral": 0.3
  },
  "trend": "BULLISH"
}
```

---

### GET /api/signals/{ticker}
**Get trading signal for a ticker**

#### Parameters
- `ticker` (path, required): Stock ticker

#### Example Request
```bash
curl http://localhost:8000/api/signals/AAPL
```

#### Response
```json
{
  "ticker": "AAPL",
  "final_signal": "BUY",
  "combined_score": 0.654,
  "technical": {
    "signal": "BUY",
    "confidence": 0.75,
    "latest_price": 150.25,
    "price_change_percent": 2.5
  },
  "sentiment": {
    "signal": "BUY",
    "articles_analyzed": 10
  },
  "weights": {
    "technical": 0.7,
    "sentiment": 0.3
  },
  "timestamp": "2026-03-06T13:30:00"
}
```

---

### GET /api/technical/{ticker}
**Get technical analysis**

#### Example Request
```bash
curl http://localhost:8000/api/technical/AAPL
```

#### Response
```json
{
  "ticker": "AAPL",
  "signal": "BUY",
  "confidence": 0.75,
  "latest_price": 150.25,
  "price_change_percent": 2.5,
  "buy_signals": 3,
  "sell_signals": 1,
  "individual_signals": {
    "rsi": "HOLD",
    "macd": "BUY",
    "moving_average": "BUY",
    "bollinger_bands": "BUY"
  },
  "technical_data": {
    "rsi": 65.4,
    "macd": { ... },
    "ma": { ... },
    "bb": { ... }
  }
}
```

---

### GET /api/market/overview
**Get overall market sentiment**

#### Parameters
- `hours` (query, optional): Hours to analyze (default: 24)

#### Example Request
```bash
curl "http://localhost:8000/api/market/overview?hours=24"
```

#### Response
```json
{
  "timestamp": "2026-03-06T13:30:00",
  "articles_analyzed": 150,
  "sentiment_distribution": {
    "positive": 93,
    "negative": 27,
    "neutral": 30
  },
  "sentiment_ratios": {
    "positive": 0.62,
    "negative": 0.18,
    "neutral": 0.2
  },
  "market_trend": "BULLISH",
  "top_sources": ["cnbc", "reuters", "bloomberg", "seeking_alpha"]
}
```

---

## Code Examples

### Python (requests)

```python
import requests

# Analyze a single ticker
response = requests.get('http://localhost:8000/api/analyze/AAPL')
result = response.json()
print(f"Signal: {result['signal']['final_signal']}")

# Analyze multiple tickers
data = {
    "tickers": ["AAPL", "MSFT", "GOOGL"],
    "hours": 24
}
response = requests.post('http://localhost:8000/api/analyze/batch', json=data)
portfolio = response.json()
print(f"Recommendation: {portfolio['summary']['recommendation']}")

# Analyze sentiment
data = {
    "title": "Apple Beats Earnings",
    "content": "Strong Q4 results"
}
response = requests.post('http://localhost:8000/api/sentiment/analyze', json=data)
sentiment = response.json()
print(f"Sentiment: {sentiment['combined_sentiment']}")
```

### JavaScript (fetch)

```javascript
// Analyze a ticker
const ticker = 'AAPL';
const response = await fetch(`http://localhost:8000/api/analyze/${ticker}`);
const analysis = await response.json();
console.log(`Signal: ${analysis.signal.final_signal}`);

// Analyze portfolio
const portfolioData = {
  tickers: ["AAPL", "MSFT", "GOOGL"],
  hours: 24
};
const response = await fetch('http://localhost:8000/api/analyze/batch', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(portfolioData)
});
const portfolio = await response.json();
console.log(`Recommendation: ${portfolio.summary.recommendation}`);
```

### cURL

```bash
# Health check
curl http://localhost:8000/health

# Analyze ticker
curl http://localhost:8000/api/analyze/AAPL

# Get market overview
curl http://localhost:8000/api/market/overview

# Get portfolio signals
curl "http://localhost:8000/api/portfolio?tickers=AAPL,MSFT,GOOGL"

# Get news
curl "http://localhost:8000/api/news/AAPL?hours=24"
```

---

## Error Handling

### Example Error Response

```json
{
  "error": "Ticker INVALID not found",
  "status_code": 500,
  "timestamp": "2026-03-06T13:30:00"
}
```

### Common Status Codes
- `200` - Success
- `400` - Bad request (invalid parameters)
- `404` - Not found
- `500` - Server error
- `503` - Service unavailable

---

## Rate Limiting & Performance

- Single ticker analysis: ~5-10 seconds
- Portfolio analysis (5 tickers): ~30-60 seconds
- Market overview: ~15-30 seconds
- Recommended: Cache results for 1-24 hours

---

## Deployment

### Local Development
```bash
python api/main.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 api.main:app
```

### Docker
```bash
docker build -f docker/Dockerfile -t stock-intel .
docker run -p 8000:8000 stock-intel
```

---

## Support & Troubleshooting

### API not starting?
```bash
# Check if port 8000 is available
lsof -i :8000

# Use different port
python api/main.py --port 8001
```

### Module import errors?
```bash
# Ensure you're in the venv
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Slow responses?
- Increase `hours` parameter to get cached results
- Run on a machine with more CPU/RAM
- Use GPU mode if available

---

## Next Steps

1. **Frontend**: Build React dashboard to visualize signals
2. **Database**: Store results in PostgreSQL for history
3. **Scheduling**: Use Celery for continuous updates
4. **Alerts**: Email/SMS notifications for strong signals
5. **Backtesting**: Test strategies on historical data

Happy API-ing! 🚀
