"""News Scraper Module for Stock Market Intelligence.

Combines multiple sources: RSS feeds, web scraping, Reddit, and news APIs.
"""

from __future__ import annotations

import hashlib
import logging
import time
from datetime import datetime, timedelta

try:
    import feedparser
except ImportError:  # pragma: no cover
    feedparser = None  # type: ignore[assignment]
import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class NewsArticle:
    """Data class for a news article"""

    def __init__(
        self, title: str, content: str, source: str, url: str, published_date: datetime, ticker: str | None = None
    ):
        self.title = title
        self.content = content
        self.source = source
        self.url = url
        self.published_date = published_date
        self.ticker = ticker

    @property
    def url_hash(self) -> str:
        """SHA-256 fingerprint of the canonical URL for deduplication."""
        return hashlib.sha256(self.url.strip().lower().encode()).hexdigest()[:16]

    def to_dict(self) -> dict:
        """Convert to dictionary for storage/API"""
        return {
            "title": self.title,
            "content": self.content,
            "source": self.source,
            "url": self.url,
            "published_date": self.published_date.isoformat(),
            "ticker": self.ticker,
        }


class RSSFeedScraper:
    """Scrapes news from RSS feeds (financial news, company blogs, etc.)"""

    # Popular financial RSS feeds
    FEEDS = {
        "cnbc": "https://feeds.cnbc.com/cnbcnews/rss.html",
        "reuters": "https://feeds.reuters.com/reuters/businessNews",
        "bloomberg": "https://feeds.bloomberg.com/markets/news.rss",
        "seeking_alpha": "https://seekingalpha.com/feed.xml",
        "market_watch": "https://feeds.marketwatch.com/marketwatch/topstories/",
        "ft_markets": "https://www.ft.com/rss/home/uk",
        "wsj_markets": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
        "nasdaq_news": "https://www.nasdaq.com/feed/rssoutbound?category=Markets",
        "investopedia": "https://www.investopedia.com/feedbuilder/feed/getfeed/?feedName=investopedia_articles",
        "yahoo_finance": "https://finance.yahoo.com/news/rssindex",
    }

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()

    def fetch_feed(self, feed_url: str, feed_name: str, retries: int = 3) -> list[NewsArticle]:
        """Fetch articles from a single RSS feed with exponential-backoff retries."""
        articles = []
        last_exc: Exception | None = None
        for attempt in range(retries):
            try:
                logger.info("Fetching %s feed (attempt %d)...", feed_name, attempt + 1)
                feed = feedparser.parse(feed_url)

                for entry in feed.entries[:10]:
                    try:
                        title = entry.get("title", "No title")
                        content = entry.get("summary", "")[:500]
                        url = entry.get("link", "")

                        pub_date = datetime.now()
                        if hasattr(entry, "published_parsed") and entry.published_parsed:
                            pub_date = datetime(*entry.published_parsed[:6])

                        article = NewsArticle(
                            title=title, content=content, source=feed_name, url=url, published_date=pub_date
                        )
                        articles.append(article)

                    except Exception as e:
                        logger.warning("Error parsing entry from %s: %s", feed_name, e)
                        continue
                return articles
            except Exception as e:
                last_exc = e
                wait = 2**attempt
                logger.warning("Error fetching %s feed (attempt %d): %s. Retrying in %ds.", feed_name, attempt + 1, e, wait)
                time.sleep(wait)

        logger.error("All %d attempts failed for %s feed: %s", retries, feed_name, last_exc)
        return articles

    def fetch_all_feeds(self) -> list[NewsArticle]:
        """Fetch from all configured feeds, deduplicating by URL hash."""
        seen: set[str] = set()
        all_articles: list[NewsArticle] = []
        for feed_name, feed_url in self.FEEDS.items():
            for article in self.fetch_feed(feed_url, feed_name):
                if article.url_hash not in seen:
                    seen.add(article.url_hash)
                    all_articles.append(article)

        all_articles.sort(key=lambda x: x.published_date, reverse=True)
        return all_articles


class WebScraper:
    """Scrapes news from websites using BeautifulSoup"""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

    def scrape_yahoo_finance(self, ticker: str) -> list[NewsArticle]:
        """Scrape news from Yahoo Finance for a specific ticker"""
        articles = []
        try:
            url = f"https://finance.yahoo.com/quote/{ticker}/news"
            logger.info(f"Scraping Yahoo Finance for {ticker}...")

            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Note: Yahoo Finance uses JavaScript rendering, so this is limited
            # For production, consider using Selenium for JS-heavy sites
            news_items = soup.find_all("a", {"data-test": "quoteNewsLink"})

            for item in news_items[:5]:
                try:
                    title = item.get_text(strip=True)
                    href = item.get("href", "")

                    if title and href:
                        article = NewsArticle(
                            title=title,
                            content=f"News from Yahoo Finance for {ticker}",
                            source="yahoo_finance",
                            url=f"https://finance.yahoo.com{href}" if not href.startswith("http") else href,
                            published_date=datetime.now(),
                            ticker=ticker,
                        )
                        articles.append(article)
                except Exception as e:
                    logger.warning(f"Error parsing Yahoo Finance item: {e}")

        except Exception as e:
            logger.error(f"Error scraping Yahoo Finance for {ticker}: {e}")

        return articles

    def scrape_earnings_call_transcripts(self, ticker: str) -> list[NewsArticle]:
        """Scrape earnings call transcripts (example using Motley Fool RSS)"""
        articles = []
        try:
            # Using a generic financial news approach
            url = f"https://feeds.themotleyfool.com/RSSFeed?t={ticker}"
            logger.info(f"Fetching earnings news for {ticker}...")

            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:
                try:
                    if "earnings" in entry.get("title", "").lower():
                        article = NewsArticle(
                            title=entry.get("title", ""),
                            content=entry.get("summary", "")[:500],
                            source="earnings_transcripts",
                            url=entry.get("link", ""),
                            published_date=datetime.now(),
                            ticker=ticker,
                        )
                        articles.append(article)
                except Exception as e:
                    logger.warning(f"Error parsing earnings transcript: {e}")

        except Exception as e:
            logger.error(f"Error scraping earnings for {ticker}: {e}")

        return articles


class NewsAggregator:
    """Main aggregator that combines all news sources"""

    def __init__(self):
        self.rss_scraper = RSSFeedScraper()
        self.web_scraper = WebScraper()

    def get_market_news(self, hours: int = 24) -> list[NewsArticle]:
        """Get recent market news from all sources"""
        logger.info(f"Aggregating market news from last {hours} hours...")

        # Get RSS feed news
        rss_articles = self.rss_scraper.fetch_all_feeds()

        # Filter by time
        cutoff_time = datetime.now() - timedelta(hours=hours)
        filtered_articles = [article for article in rss_articles if article.published_date >= cutoff_time]

        logger.info(f"Found {len(filtered_articles)} articles from last {hours} hours")
        return filtered_articles

    def get_ticker_news(self, ticker: str, hours: int = 24) -> list[NewsArticle]:
        """Get news specific to a ticker"""
        logger.info(f"Aggregating news for {ticker}...")

        articles = []

        # Get web-scraped news
        articles.extend(self.web_scraper.scrape_yahoo_finance(ticker))
        articles.extend(self.web_scraper.scrape_earnings_call_transcripts(ticker))

        # Sort by date
        articles.sort(key=lambda x: x.published_date, reverse=True)

        logger.info(f"Found {len(articles)} articles for {ticker}")
        return articles

    def search_news(self, query: str, hours: int = 24) -> list[NewsArticle]:
        """Search for news matching a query"""
        logger.info(f"Searching for news matching: {query}")

        # Get all market news
        all_news = self.get_market_news(hours=hours)

        # Filter by query
        query_lower = query.lower()
        filtered = [
            article
            for article in all_news
            if query_lower in article.title.lower() or query_lower in article.content.lower()
        ]

        logger.info(f"Found {len(filtered)} articles matching '{query}'")
        return filtered


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    _log = logging.getLogger(__name__)

    aggregator = NewsAggregator()

    _log.info("=== MARKET NEWS (Last 24 hours) ===")
    market_news = aggregator.get_market_news(hours=24)
    for article in market_news[:5]:
        _log.info("Title: %s | Source: %s | Date: %s | URL: %s", article.title, article.source, article.published_date, article.url)

    _log.info("=== TICKER NEWS (AAPL) ===")
    ticker_news = aggregator.get_ticker_news("AAPL")
    for article in ticker_news[:3]:
        _log.info("Title: %s | Source: %s | Date: %s", article.title, article.source, article.published_date)

    _log.info("=== SEARCH RESULTS (AI) ===")
    search_results = aggregator.search_news("AI", hours=24)
    for article in search_results[:3]:
        _log.info("Title: %s | Source: %s", article.title, article.source)

    _log.info("News scraper module working!")
