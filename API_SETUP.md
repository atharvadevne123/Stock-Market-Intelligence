# Stock Market Intelligence API - Setup Guide

## 📋 What You Now Have

You've built a **production-ready REST API** with:

✅ 20+ endpoints for analysis, news, sentiment, signals, and technical analysis  
✅ Interactive Swagger UI documentation at `/docs`  
✅ Error handling and logging  
✅ CORS support for frontend integration  
✅ Pydantic models for request/response validation  

---

## 🚀 Quick Start (5 minutes)

### Step 1: Copy API Files to Your Project

Copy these files to your project structure:

```
Stock Market Intelligence/
├── api/
│   ├── __init__.py          ← Create this
│   └── main.py              ← Copy api_main.py here and rename
├── scraper/
│   ├── __init__.py
│   └── news_scraper.py
├── nlp/
│   ├── __init__.py
│   └── sentiment_analyzer.py
├── analysis/
│   ├── __init__.py
│   └── signal_engine.py
├── main_orchestrator.py
├── requirements.txt
└── .env.example
```

### Step 2: Create API Directory and Files

```bash
cd "/Users/atharvadevne/Python/Stock Market Intelligence"

# Create api directory
mkdir -p api
touch api/__init__.py

# Copy the api_main.py to api/main.py
cp api_main.py api/main.py
```

### Step 3: Start the API

```bash
# Activate venv
source venv/bin/activate

# Start API server
python api/main.py
```

You should see:

```
╔════════════════════════════════════════════════════════════════╗
║  STARTING STOCK MARKET INTELLIGENCE API                       ║
╚════════════════════════════════════════════════════════════════╝

📍 API will be available at: http://localhost:8000
📚 Interactive docs at: http://localhost:8000/docs
📖 ReDoc docs at: http://localhost:8000/redoc
```

### Step 4: Test the API

Open in your browser:
- **Interactive API Explorer**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

Or test from terminal:

```bash
# Test health endpoint
curl http://localhost:8000/health

# Analyze AAPL
curl http://localhost:8000/api/analyze/AAPL

# Get market overview
curl http://localhost:8000/api/market/overview

# Get portfolio signals
curl "http://localhost:8000/api/portfolio?tickers=AAPL,MSFT,GOOGL"
```

---

## 📚 Key API Endpoints

### Analysis
```
GET  /api/analyze/{ticker}           # Analyze single stock
POST /api/analyze/batch              # Analyze multiple stocks
GET  /api/portfolio                  # Portfolio analysis
```

### News
```
GET  /api/news/market                # Get market news
GET  /api/news/{ticker}              # Get ticker news
GET  /api/news/search                # Search news
```

### Sentiment
```
POST /api/sentiment/analyze          # Analyze article sentiment
GET  /api/sentiment/{ticker}         # Get ticker sentiment trend
```

### Signals
```
GET  /api/signals/{ticker}           # Get trading signal
POST /api/signals/batch              # Get signals for multiple tickers
GET  /api/signals/interpretation     # Explain signals
```

### Technical
```
GET  /api/technical/{ticker}         # Get technical indicators
```

### Market
```
GET  /api/market/overview            # Market sentiment & trends
```

---

## 🔌 Example API Calls

### Python

```python
import requests

# Analyze a stock
response = requests.get('http://localhost:8000/api/analyze/AAPL?hours=24')
result = response.json()

print(f"Ticker: {result['ticker']}")
print(f"Signal: {result['signal']['final_signal']}")
print(f"Price: ${result['signal']['technical']['latest_price']}")
print(f"Change: {result['signal']['technical']['price_change_percent']}%")
```

### JavaScript

```javascript
// Analyze a portfolio
const response = await fetch('http://localhost:8000/api/portfolio?tickers=AAPL,MSFT,GOOGL');
const portfolio = await response.json();

console.log(`Recommendation: ${portfolio.summary.recommendation}`);
console.log(`Signals:`, portfolio.summary.signal_distribution);
```

### cURL

```bash
# Get sentiment for a ticker
curl "http://localhost:8000/api/sentiment/AAPL?hours=48"

# Analyze multiple tickers
curl -X POST http://localhost:8000/api/analyze/batch \
  -H "Content-Type: application/json" \
  -d '{"tickers": ["AAPL", "MSFT", "GOOGL"], "hours": 24}'

# Get market trend
curl http://localhost:8000/api/market/overview
```

---

## 🛠️ API Architecture

### Request Flow

```
Client Request
    ↓
FastAPI Router
    ↓
Pydantic Validation
    ↓
Business Logic (Main Orchestrator)
    ↓
Components (Scraper, Sentiment, Signals)
    ↓
Response (JSON)
```

### File Structure

```
api/
├── main.py                 # Main FastAPI application
│   ├── Health endpoints
│   ├── Analysis endpoints
│   ├── News endpoints
│   ├── Sentiment endpoints
│   ├── Signal endpoints
│   ├── Technical endpoints
│   ├── Market endpoints
│   └── Utility endpoints
└── __init__.py
```

---

## 📊 Response Format

### Successful Response (200 OK)

```json
{
  "ticker": "AAPL",
  "signal": {
    "final_signal": "BUY",
    "combined_score": 0.654,
    "confidence": 0.75
  }
}
```

### Error Response (5xx)

```json
{
  "error": "Internal server error",
  "status_code": 500,
  "timestamp": "2026-03-06T13:30:00"
}
```

---

## ⚙️ Configuration

### Environment Variables (.env)

Create a `.env` file (copy from `.env.example`):

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_ENVIRONMENT=development
API_LOG_LEVEL=INFO

# Model Configuration
DEVICE=cpu
USE_GPU=False

# Data Settings
DEFAULT_HOURS_LOOKBACK=24
MAX_ARTICLES_PER_TICKER=50
```

---

## 🚀 Deployment Options

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
# Build image
docker build -f docker/Dockerfile -t stock-intel:latest .

# Run container
docker run -p 8000:8000 stock-intel:latest
```

### Cloud Deployment (AWS, Heroku, etc.)
See deployment documentation for your platform.

---

## 🔍 Monitoring & Debugging

### View Logs
```bash
# API logs are printed to console
# Check for errors and INFO messages
```

### Performance Testing
```bash
# Install Apache Bench
brew install httpd

# Load test the API
ab -n 100 -c 10 http://localhost:8000/api/analyze/AAPL
```

### API Health Check
```bash
curl http://localhost:8000/health
```

---

## 🔐 Security (For Production)

### Enable API Key Authentication
Uncomment in `api/main.py`:
```python
ENABLE_API_KEY_AUTH=True
```

### CORS Configuration
Update in `api/main.py`:
```python
CORS_ORIGINS=["https://yourdomain.com"]
```

### HTTPS
Use a reverse proxy (nginx) or AWS API Gateway.

---

## 🧪 Testing the API

### Using Swagger UI
1. Go to http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"

### Using Python
```python
import requests

# Test all endpoints
endpoints = [
    '/health',
    '/api/analyze/AAPL',
    '/api/news/market',
    '/api/market/overview'
]

for endpoint in endpoints:
    response = requests.get(f'http://localhost:8000{endpoint}')
    print(f"{endpoint}: {response.status_code}")
```

---

## 📝 API Response Examples

### /api/analyze/AAPL
```json
{
  "ticker": "AAPL",
  "signal": {
    "final_signal": "BUY",
    "combined_score": 0.654,
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

### /api/sentiment/{ticker}
```json
{
  "ticker": "AAPL",
  "articles_analyzed": 10,
  "sentiment_distribution": {
    "positive": 6,
    "negative": 1,
    "neutral": 3
  },
  "trend": "BULLISH"
}
```

### /api/market/overview
```json
{
  "market_trend": "BULLISH",
  "articles_analyzed": 150,
  "sentiment_ratios": {
    "positive": 0.62,
    "negative": 0.18,
    "neutral": 0.20
  }
}
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
python api/main.py --port 8001
```

### Import Errors
```bash
# Ensure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Slow Responses
- API is likely downloading models or scraping news
- First request takes longer (FinBERT model download)
- Subsequent requests are faster
- Consider adding caching for production

### Module Not Found Errors
```bash
# Make sure __init__.py files exist in all directories
touch scraper/__init__.py
touch nlp/__init__.py
touch analysis/__init__.py
touch api/__init__.py
```

---

## 📚 Full Documentation

See `API_DOCUMENTATION.md` for:
- Complete endpoint reference
- Request/response examples
- Code examples in Python, JavaScript, cURL
- Error handling
- Rate limiting info

---

## 🎯 Next Steps

With the API running, you can now:

1. **Build Frontend**: React dashboard to visualize signals
2. **Add Database**: PostgreSQL to store historical data
3. **Schedule Tasks**: Celery for continuous updates
4. **Send Alerts**: Email/SMS for strong signals
5. **Backtest**: Historical analysis

---

## 🎉 You're Done!

You now have a fully functional **Stock Market Intelligence REST API**!

**Start the API:**
```bash
source venv/bin/activate
python api/main.py
```

**Access the docs:**
http://localhost:8000/docs

**Analyze stocks:**
```bash
curl http://localhost:8000/api/analyze/AAPL
```

Happy analyzing! 🚀📈
