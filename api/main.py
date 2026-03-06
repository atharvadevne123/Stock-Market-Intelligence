"""
Stock Market Intelligence - FastAPI Backend
Simplified version without database dependency
"""

import logging
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Stock Market Intelligence API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import core components
try:
    from scraper.news_scraper import NewsAggregator
    from nlp.sentiment_analyzer import NewsArticleSentimentAnalyzer
    from analysis.signal_engine import ComprehensiveSignalEngine
    from main_orchestrator import StockMarketIntelligence
    logger.info("✅ All modules imported")
except Exception as e:
    logger.error(f"Import error: {e}")
    raise

class PortfolioRequest(BaseModel):
    tickers: List[str]
    hours: int = 24

# Initialize
system = None
signal_engine = None

@app.on_event("startup")
async def startup():
    global system, signal_engine
    logger.info("Initializing system...")
    try:
        system = StockMarketIntelligence()
        signal_engine = ComprehensiveSignalEngine()
        logger.info("✅ System ready")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise

@app.get("/")
async def root():
    return {"name": "Stock Market Intelligence API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/analyze/{ticker}")
async def analyze_ticker(ticker: str, hours: int = Query(24)):
    try:
        logger.info(f"Analyzing {ticker}")
        result = system.analyze_ticker(ticker, hours=hours)
        return result
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/portfolio")
async def get_portfolio(tickers: str = Query(...), hours: int = Query(24)):
    try:
        ticker_list = [t.strip().upper() for t in tickers.split(",")]
        result = system.analyze_portfolio(ticker_list, hours=hours)
        return result
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/market/overview")
async def market_overview(hours: int = Query(24)):
    try:
        return system.get_market_overview(hours=hours)
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/signals/{ticker}")
async def get_signal(ticker: str):
    try:
        result = signal_engine.generate_signal(ticker)
        return result
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/technical/{ticker}")
async def get_technical(ticker: str):
    try:
        result = signal_engine.technical_generator.generate_technical_signal(ticker)
        return result
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*80)
    print("STOCK MARKET INTELLIGENCE API")
    print("="*80)
    print("\n📍 API: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("\n" + "="*80 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
