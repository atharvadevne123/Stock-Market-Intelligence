#!/usr/bin/env python3
"""Stock Market Intelligence - Quick Start Guide.

Run this script to verify the environment and demonstrate the system.
"""

from __future__ import annotations

import logging
import sys

logging.basicConfig(level=logging.INFO)
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
    print("=" * 80)
    print("CHECKING ENVIRONMENT")
    print("=" * 80)
    missing: list[str] = []
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
            print(f"  OK  {package}")
        except ImportError:
            print(f"  MISSING  {package}")
            missing.append(package)
    return missing


def demo_news_scraper() -> None:
    """Demonstrate the news scraper with a sample ticker."""
    print("=" * 80)
    print("DEMO: NEWS SCRAPER")
    print("=" * 80)
    try:
        from scraper.news_scraper import NewsAggregator

        aggregator = NewsAggregator()
        articles = aggregator.get_ticker_news("AAPL", hours=6)
        print(f"  Found {len(articles)} articles for AAPL (last 6h)")
        for a in articles[:3]:
            print(f"  - {a.title[:80]}")
    except Exception:
        logger.exception("News scraper demo failed")


def demo_technical_analysis() -> None:
    """Demonstrate the technical signal engine."""
    print("=" * 80)
    print("DEMO: TECHNICAL ANALYSIS")
    print("=" * 80)
    try:
        from analysis.signal_engine import ComprehensiveSignalEngine

        engine = ComprehensiveSignalEngine()
        result = engine.technical_generator.generate_technical_signal("AAPL")
        print(f"  Signal: {result.get('signal')}")
        print(f"  Price:  ${result.get('latest_price')}")
        print(f"  Change: {result.get('price_change_percent')}%")
    except Exception:
        logger.exception("Technical analysis demo failed")


def main() -> int:
    """Entry point."""
    missing = check_environment()
    if missing:
        print(f"\nInstall missing packages: pip install {' '.join(missing)}")
        return 1

    demo_news_scraper()
    demo_technical_analysis()
    print("\nQuick start complete. Run `make run` to start the API server.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
