"""FastAPI application for the Stock Market Intelligence platform."""
from __future__ import annotations

import logging
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Globals populated during lifespan startup
# ---------------------------------------------------------------------------
system = None
signal_engine = None
_request_count = 0
_error_count = 0
_start_time: float = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialise heavy components once at startup and release at shutdown."""
    global system, signal_engine
    logger.info("Starting Stock Market Intelligence API…")
    try:
        from analysis.signal_engine import ComprehensiveSignalEngine
        from main_orchestrator import StockMarketIntelligence
        from scraper.news_scraper import NewsAggregator  # noqa: F401 – validates import

        system = StockMarketIntelligence()
        signal_engine = ComprehensiveSignalEngine()
        logger.info("System ready")
    except Exception:
        logger.exception("Startup failed")
        raise
    yield
    logger.info("Shutting down…")


app = FastAPI(
    title="Stock Market Intelligence API",
    version="1.0.0",
    description=(
        "Real-time stock market intelligence combining FinBERT sentiment analysis, "
        "technical indicators, and live news scraping to generate BUY/SELL/HOLD signals."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next) -> Response:
    """Attach a correlation ID to every request for distributed tracing."""
    global _request_count, _error_count
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    _request_count += 1
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    if response.status_code >= 500:
        _error_count += 1
    response.headers["X-Correlation-ID"] = correlation_id
    response.headers["X-Response-Time-Ms"] = f"{duration_ms:.1f}"
    logger.debug(
        "%-6s %s → %d (%.1fms) [%s]",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
        correlation_id,
    )
    return response


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------
class PortfolioRequest(BaseModel):
    tickers: list[str] = Field(..., min_length=1, max_length=50)
    hours: int = Field(24, ge=1, le=720)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/", summary="Service banner")
async def root() -> dict:
    return {"name": "Stock Market Intelligence API", "status": "running"}


@app.get("/health", summary="Health check")
async def health() -> dict:
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/api/version", summary="API version and uptime")
async def version() -> dict:
    """Return the API version, Python runtime info, and uptime seconds."""
    import sys

    return {
        "version": "1.0.0",
        "python": sys.version.split()[0],
        "uptime_seconds": round(time.time() - _start_time, 1),
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/metrics", summary="Runtime request metrics")
async def metrics() -> dict:
    """Return basic request / error counters for monitoring dashboards."""
    return {
        "requests_total": _request_count,
        "errors_total": _error_count,
        "uptime_seconds": round(time.time() - _start_time, 1),
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/analyze/{ticker}", summary="Full analysis for a ticker")
async def analyze_ticker(
    ticker: str,
    hours: int = Query(24, ge=1, le=720, description="Hours of news to include"),
) -> dict:
    """Run the complete analysis pipeline (news → sentiment → signal) for *ticker*."""
    try:
        logger.info("Analysing %s", ticker.upper())
        return system.analyze_ticker(ticker.upper(), hours=hours)
    except Exception:
        logger.exception("Error analysing %s", ticker)
        raise HTTPException(status_code=500, detail="Analysis failed")


@app.get("/api/portfolio", summary="Portfolio analysis for multiple tickers")
async def get_portfolio(
    tickers: str = Query(..., description="Comma-separated ticker symbols"),
    hours: int = Query(24, ge=1, le=720),
) -> dict:
    """Analyse a portfolio of tickers and return an aggregate summary."""
    try:
        ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
        if not ticker_list:
            raise HTTPException(status_code=422, detail="No valid tickers supplied")
        return system.analyze_portfolio(ticker_list, hours=hours)
    except HTTPException:
        raise
    except Exception:
        logger.exception("Portfolio analysis failed")
        raise HTTPException(status_code=500, detail="Portfolio analysis failed")


@app.get("/api/market/overview", summary="Market-wide sentiment overview")
async def market_overview(
    hours: int = Query(24, ge=1, le=720),
) -> dict:
    """Aggregate sentiment across the latest market news."""
    try:
        return system.get_market_overview(hours=hours)
    except Exception:
        logger.exception("Market overview failed")
        raise HTTPException(status_code=500, detail="Market overview failed")


@app.get("/api/signals/{ticker}", summary="Combined technical and sentiment signal")
async def get_signal(ticker: str) -> dict:
    """Generate a comprehensive trading signal for *ticker*."""
    try:
        return signal_engine.generate_signal(ticker.upper())
    except Exception:
        logger.exception("Signal generation failed for %s", ticker)
        raise HTTPException(status_code=500, detail="Signal generation failed")


@app.get("/api/technical/{ticker}", summary="Technical indicator analysis")
async def get_technical(ticker: str) -> dict:
    """Return raw technical indicator values and the derived signal for *ticker*."""
    try:
        return signal_engine.technical_generator.generate_technical_signal(ticker.upper())
    except Exception:
        logger.exception("Technical analysis failed for %s", ticker)
        raise HTTPException(status_code=500, detail="Technical analysis failed")


if __name__ == "__main__":
    import uvicorn

    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8000)
