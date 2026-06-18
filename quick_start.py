#!/usr/bin/env python3
"""Stock Market Intelligence - Quick Start Guide.

Run this script to verify the environment and demonstrate the system.
"""

from __future__ import annotations

import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

REQUIRED_PACKAGES: list[str] = [
    "requests",
    "beautifulsoup4",
    "feedparser",
    "pandas",
    "yfinance",
    "transformers",
    "torch",
    "fastapi",
    "sqlalchemy",
    "praw",
]


def check_environment() -> list[str]:
    """Check which required packages are importable.

    Returns:
        List of missing package names.
    """
    logger.info("=" * 60)
    logger.info("CHECKING ENVIRONMENT")
    logger.info("=" * 60)
    missing: list[str] = []
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
            logger.info("  OK  %s", package)
        except ImportError:
            logger.warning("  MISSING  %s", package)
            missing.append(package)
    return missing


def demo_news_scraper() -> None:
    """Demonstrate the news scraper with a sample ticker."""
    logger.info("=" * 60)
    logger.info("DEMO: NEWS SCRAPER")
    logger.info("=" * 60)
    try:
        from scraper.news_scraper import NewsAggregator

        aggregator = NewsAggregator()
        articles = aggregator.get_ticker_news("AAPL", hours=6)
        logger.info("Found %d articles for AAPL (last 6h)", len(articles))
        for a in articles[:3]:
            logger.info("  - %s", a.title[:80])
    except Exception:
        logger.exception("News scraper demo failed")


def demo_technical_analysis() -> None:
    """Demonstrate the technical signal engine."""
    logger.info("=" * 60)
    logger.info("DEMO: TECHNICAL ANALYSIS")
    logger.info("=" * 60)
    try:
        from analysis.signal_engine import ComprehensiveSignalEngine

        engine = ComprehensiveSignalEngine()
        result = engine.technical_generator.generate_technical_signal("AAPL")
        logger.info("Signal: %s", result.get("signal"))
        logger.info("Price:  $%s", result.get("latest_price"))
        logger.info("Change: %s%%", result.get("price_change_percent"))
    except Exception:
        logger.exception("Technical analysis demo failed")


def main() -> int:
    """Entry point."""
    missing = check_environment()
    if missing:
        logger.error("Install missing packages: pip install %s", " ".join(missing))
        return 1

    demo_news_scraper()
    demo_technical_analysis()
    logger.info("Quick start complete. Run `make run` to start the API server.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
