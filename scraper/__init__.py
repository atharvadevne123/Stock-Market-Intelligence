"""News scraping and aggregation package.

Provides NewsAggregator which combines RSS feed scraping,
Yahoo Finance web scraping, and earnings call transcript
scraping into a unified article stream.
"""

from __future__ import annotations

from .news_scraper import NewsAggregator, NewsArticle, RSSFeedScraper, WebScraper

__version__ = "1.0.0"
__all__ = ["NewsAggregator", "NewsArticle", "RSSFeedScraper", "WebScraper"]
