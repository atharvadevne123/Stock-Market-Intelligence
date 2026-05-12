# Changelog

All notable changes to Stock Market Intelligence are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive test suite covering signal engine, API, database, scraper, and sentiment
- GitHub Actions CI workflow with lint, test, and type-check jobs
- Makefile with `install`, `test`, `coverage`, `lint`, `format`, `run`, `docker-build` targets
- CONTRIBUTING.md with development workflow guidelines
- Dockerfile and docker-compose.yml for containerised deployment
- `.pre-commit-config.yaml` with ruff and trailing-whitespace hooks
- Type annotations across all core modules
- Google-style docstrings for all public classes and functions
- Structured logging replacing `print()` calls in `api/database.py` and `database/models.py`
- `/api/version` and `/api/metrics` endpoints
- Correlation ID middleware for request tracing
- `functools.lru_cache` on `_signal_to_score` for efficiency
- `get_db` FastAPI dependency for database session management
- Database indexes on `ticker` and `created_at` columns
- Input validation and improved error handling throughout
- `.env.example` with all required environment variables documented
- `pyproject.toml` now includes `[tool.ruff]`, `[tool.pytest.ini_options]`, and `[tool.mypy]`

## [1.0.0] - 2024-11-01

### Added
- Initial release
- FinBERT sentiment analysis of financial news articles
- Technical indicator signal engine (RSI, MACD, Bollinger Bands, Moving Averages)
- FastAPI backend with `/analyze`, `/signals`, `/technical`, `/portfolio`, `/health` endpoints
- RSS feed scraper and Yahoo Finance web scraper
- SQLAlchemy models for Articles, Signals, Sentiments, Portfolios, and Backtest Results
- Main orchestrator combining all components
- Frontend Vue.js globe visualization
- Docker support
- Alembic migrations
