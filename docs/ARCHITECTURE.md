# Architecture Overview

## System Layers

```
┌─────────────────────────────────────────────────┐
│                  FastAPI (api/)                  │
│  /health  /api/analyze  /api/signals  /api/tech  │
│  /api/portfolio  /api/portfolio/risk             │
└────────────────────┬────────────────────────────┘
                     │
       ┌─────────────┴─────────────┐
       │                           │
┌──────┴──────┐           ┌────────┴────────┐
│  analysis/  │           │   scraper/      │
│  signal_    │           │   news_scraper  │
│  engine.py  │           │   (RSS + Web)   │
│  portfolio_ │           └────────┬────────┘
│  risk.py    │                    │
│  performance│           ┌────────┴────────┐
│  _metrics.py│           │     nlp/        │
└──────┬──────┘           │  sentiment_     │
       │                  │  analyzer.py    │
       └──────────────────┘  (FinBERT)
                     │
             ┌───────┴──────┐
             │  database/   │
             │  models.py   │
             │  SQLAlchemy  │
             └──────────────┘
```

## Key Components

### api/
- `main.py` — FastAPI app, lifespan, endpoints, ticker validation
- `database.py` — `DatabaseService` static methods (save/get articles, signals, watchlists)
- `schemas.py` — Pydantic response models

### analysis/
- `signal_engine.py` — `ComprehensiveSignalEngine`, `TechnicalIndicator`, `TechnicalSignalGenerator`, `SentimentSignalGenerator`
- `portfolio_risk.py` — `PortfolioRiskCalculator` (VaR, Sharpe, drawdown, correlation)
- `performance_metrics.py` — `PerformanceMetrics` (CAGR, Sortino, Calmar)

### scraper/
- `news_scraper.py` — `RSSFeedScraper`, `WebScraper`, `NewsAggregator`; URL-hash deduplication, exponential-backoff retries

### nlp/
- `sentiment_analyzer.py` — `FinBERTSentimentAnalyzer`, `NewsArticleSentimentAnalyzer`; batch processing, confidence threshold filtering

### database/
- `models.py` — SQLAlchemy ORM models: `Article`, `Signal`, `WatchList`, `UserPreferences`

### cache/
- `ttl_cache.py` — `TTLCache` thread-safe in-memory cache with per-entry TTL and max-size LRU eviction

### scheduler/
- `__init__.py` — `PeriodicTask`, `RetryableTask`, `TaskRegistry`

### utils/
- `formatters.py` — `format_currency`, `format_percentage`, `format_signal_label`

## Data Flow

1. **News ingestion**: `RSSFeedScraper` polls feeds → `NewsAggregator` deduplicates by URL hash → `DatabaseService.save_article`
2. **Sentiment scoring**: `NewsArticleSentimentAnalyzer.analyze_article` / `analyze_articles_batch` → article dicts with `combined_sentiment`
3. **Signal generation**: `SentimentSignalGenerator.generate_sentiment_signal` + `TechnicalSignalGenerator.generate_technical_signal` → `ComprehensiveSignalEngine.generate_signal`
4. **Risk metrics**: `PortfolioRiskCalculator.summary` + `PerformanceMetrics.summary` → `/api/portfolio/risk/{ticker}` response

## Deployment

See `Dockerfile` and `docker-compose.yml` for containerised deployment. The API is served by Uvicorn on port 8000.
