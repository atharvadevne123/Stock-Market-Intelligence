# Changelog

All notable changes to Stock Market Intelligence are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added (2026-06-18)
- **WatchList and UserPreferences ORM models** — named ticker watchlists and key-value user settings
- **`/health/detailed` endpoint** — per-component health status (API, signal engine, orchestrator)
- **Ticker symbol regex validation** — `_validate_ticker()` enforces `^[A-Z]{1,5}(\.[A-Z]{1,2})?$` on all ticker endpoints
- **Stochastic oscillator and Williams %R** — new indicators in `TechnicalIndicator`
- **`analyze_stochastic` and `analyze_williams_r`** — signal generators in `TechnicalSignalGenerator`
- **`analyze_volume` and `calculate_position_size`** — volume trend confirmation and ATR-based sizing
- **`RetryableTask` and `TaskRegistry`** — exponential-backoff retry and multi-task registry in `scheduler`
- **`confidence_threshold` filtering** — `NewsArticleSentimentAnalyzer` discards low-confidence results
- **`analyze_articles_batch`** — bulk article sentiment analysis
- **URL hash deduplication** — `NewsArticle.url_hash` property; `RSSFeedScraper.fetch_all_feeds` deduplicates
- **Retry logic in `RSSFeedScraper.fetch_feed`** — up to 3 attempts with exponential backoff
- **`get_recent_signals`, `delete_old_articles`, `get_signal_aggregation_by_date`** — new `DatabaseService` methods
- **GitHub issue templates** — bug report and feature request templates
- **GitHub PR template** — standard checklist-based PR description
- **CODEOWNERS** — automatic review assignment
- **CODE_OF_CONDUCT.md** — Contributor Covenant
- **150+ new tests** — scheduler, technical indicators, API ticker validation, DB service methods, sentiment threshold

### Changed (2026-06-18)
- `scraper/news_scraper.py` — replaced `print()` with structured logging in `__main__` block
- `quick_start.py` — replaced all `print()` calls with `logging` calls
- `api/main.py` — added `re` import; endpoints raise 422 on invalid ticker symbols

## [Unreleased — 2026-05-12]

### Added
- **Test suite** — 60+ tests across signal engine, API, database, scraper, sentiment, and integration
- **GitHub Actions CI** — lint, test (3.10/3.11/3.12), type-check, and Codecov upload
- **Makefile** — `install`, `install-dev`, `test`, `coverage`, `lint`, `format`, `audit`, `run`, `run-prod`, `docker-build`, `docker-up`
- **CONTRIBUTING.md** — development workflow, commit conventions, PR process
- **Dockerfile** — multi-stage build with health check
- **docker-compose.yml** — API + PostgreSQL with health checks
- **`.pre-commit-config.yaml`** — ruff, mypy, and whitespace hooks
- **`/api/version`** endpoint — returns version, Python info, uptime
- **`/api/metrics`** endpoint — request and error counters
- **Correlation ID middleware** — attaches `X-Correlation-ID` to all responses
- **Lifespan handler** — replaces deprecated `@app.on_event("startup")`
- **`get_db` dependency** — proper FastAPI session lifecycle management
- **`get_signal_count`** and **`get_recent_articles`** — new DatabaseService methods
- **`PeriodicTask` scheduler** — thread-safe background task runner in `scheduler/__init__.py`
- **`functools.lru_cache`** on `_signal_to_score` for O(1) repeated calls
- **UTC-aware datetimes** — replaced `datetime.utcnow()` with `datetime.now(tz=timezone.utc)`
- **Composite database indexes** — `(ticker, published_date)`, `(ticker, created_at)` for fast queries
- **`__repr__` methods** on all ORM models
- **`env.example`** fully documented with all configuration options

### Changed
- `database/models.py` — migrated from deprecated `declarative_base()` to `DeclarativeBase`
- `api/database.py` — all `print()` calls replaced with structured logging
- `analysis/signal_engine.py` — `from __future__ import annotations`, modern type hints throughout
- `nlp/sentiment_analyzer.py` — lazy-imported heavy deps (torch, transformers) inside methods
- `main_orchestrator.py` — graceful per-article error handling in sentiment pipeline
- `debug_sentiment.py` — converted to proper CLI with `argparse`
- `quick_start.py` — added full type annotations
- `requirements.txt` — added `cffi`, `httpx`, `pytest-asyncio`, `pre-commit`
- `pyproject.toml` — added `[tool.ruff]`, `[tool.pytest.ini_options]`, `[tool.mypy]`, `[tool.coverage]`

### Fixed
- `api/main.py` — removed deprecated `@app.on_event` lifecycle hooks

## [1.0.0] - 2024-11-01

### Added
- Initial release with FinBERT sentiment analysis, technical indicators, FastAPI backend,
  RSS/Yahoo/Reddit news scraping, SQLAlchemy models, Vue.js globe visualization, and Docker support
