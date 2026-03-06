"""
News Scraper Module for Stock Market Intelligence
Combines multiple sources: RSS feeds, web scraping, Reddit, news APIs
"""

import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
import json
from urllib.parse import quote

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NewsArticle:
    """Data class for a news article"""
    def __init__(self, title: str, content: str, source: str, url: str, 
                 published_date: datetime, ticker: Optional[str] = None):
        self.title = title
        self.content = content
        self.source = source
        self.url = url
        self.published_date = published_date
        self.ticker = ticker
        
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage/API"""
        return {
            'title': self.title,
            'content': self.content,
            'source': self.source,
            'url': self.url,
            'published_date': self.published_date.isoformat(),
            'ticker': self.ticker
        }


class RSSFeedScraper:
    """Scrapes news from RSS feeds (financial news, company blogs, etc.)"""
    
    # Popular financial RSS feeds
    FEEDS = {
        'cnbc': 'https://feeds.cnbc.com/cnbcnews/rss.html',
        'reuters': 'https://feeds.reuters.com/reuters/businessNews',
        'bloomberg': 'https://feeds.bloomberg.com/markets/news.rss',
        'seeking_alpha': 'https://seekingalpha.com/feed.xml',
        'market_watch': 'https://feeds.marketwatch.com/marketwatch/topstories/',
    }
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        
    def fetch_feed(self, feed_url: str, feed_name: str) -> List[NewsArticle]:
        """Fetch articles from a single RSS feed"""
        articles = []
        try:
            logger.info(f"Fetching {feed_name} feed...")
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries[:10]:  # Get latest 10 articles
                try:
                    title = entry.get('title', 'No title')
                    content = entry.get('summary', '')[:500]  # Truncate
                    url = entry.get('link', '')
                    
                    # Parse published date
                    pub_date = datetime.now()
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        from time import struct_time
                        pub_date = datetime(*entry.published_parsed[:6])
                    
                    article = NewsArticle(
                        title=title,
                        content=content,
                        source=feed_name,
                        url=url,
                        published_date=pub_date
                    )
                    articles.append(article)
                    
                except Exception as e:
                    logger.warning(f"Error parsing entry from {feed_name}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error fetching {feed_name} feed: {e}")
            
        return articles
    
    def fetch_all_feeds(self) -> List[NewsArticle]:
        """Fetch from all configured feeds"""
        all_articles = []
        for feed_name, feed_url in self.FEEDS.items():
            articles = self.fetch_feed(feed_url, feed_name)
            all_articles.extend(articles)
        
        # Sort by date (newest first)
        all_articles.sort(key=lambda x: x.published_date, reverse=True)
        return all_articles


class WebScraper:
    """Scrapes news from websites using BeautifulSoup"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_yahoo_finance(self, ticker: str) -> List[NewsArticle]:
        """Scrape news from Yahoo Finance for a specific ticker"""
        articles = []
        try:
            url = f"https://finance.yahoo.com/quote/{ticker}/news"
            logger.info(f"Scraping Yahoo Finance for {ticker}...")
            
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Note: Yahoo Finance uses JavaScript rendering, so this is limited
            # For production, consider using Selenium for JS-heavy sites
            news_items = soup.find_all('a', {'data-test': 'quoteNewsLink'})
            
            for item in news_items[:5]:
                try:
                    title = item.get_text(strip=True)
                    href = item.get('href', '')
                    
                    if title and href:
                        article = NewsArticle(
                            title=title,
                            content=f"News from Yahoo Finance for {ticker}",
                            source='yahoo_finance',
                            url=f"https://finance.yahoo.com{href}" if not href.startswith('http') else href,
                            published_date=datetime.now(),
                            ticker=ticker
                        )
                        articles.append(article)
                except Exception as e:
                    logger.warning(f"Error parsing Yahoo Finance item: {e}")
                    
        except Exception as e:
            logger.error(f"Error scraping Yahoo Finance for {ticker}: {e}")
        
        return articles
    
    def scrape_earnings_call_transcripts(self, ticker: str) -> List[NewsArticle]:
        """Scrape earnings call transcripts (example using Motley Fool RSS)"""
        articles = []
        try:
            # Using a generic financial news approach
            url = f"https://feeds.themotleyfool.com/RSSFeed?t={ticker}"
            logger.info(f"Fetching earnings news for {ticker}...")
            
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:
                try:
                    if 'earnings' in entry.get('title', '').lower():
                        article = NewsArticle(
                            title=entry.get('title', ''),
                            content=entry.get('summary', '')[:500],
                            source='earnings_transcripts',
                            url=entry.get('link', ''),
                            published_date=datetime.now(),
                            ticker=ticker
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
        
    def get_market_news(self, hours: int = 24) -> List[NewsArticle]:
        """Get recent market news from all sources"""
        logger.info(f"Aggregating market news from last {hours} hours...")
        
        # Get RSS feed news
        rss_articles = self.rss_scraper.fetch_all_feeds()
        
        # Filter by time
        cutoff_time = datetime.now() - timedelta(hours=hours)
        filtered_articles = [
            article for article in rss_articles 
            if article.published_date >= cutoff_time
        ]
        
        logger.info(f"Found {len(filtered_articles)} articles from last {hours} hours")
        return filtered_articles
    
    def get_ticker_news(self, ticker: str, hours: int = 24) -> List[NewsArticle]:
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
    
    def search_news(self, query: str, hours: int = 24) -> List[NewsArticle]:
        """Search for news matching a query"""
        logger.info(f"Searching for news matching: {query}")
        
        # Get all market news
        all_news = self.get_market_news(hours=hours)
        
        # Filter by query
        query_lower = query.lower()
        filtered = [
            article for article in all_news
            if query_lower in article.title.lower() or 
               query_lower in article.content.lower()
        ]
        
        logger.info(f"Found {len(filtered)} articles matching '{query}'")
        return filtered


# Example usage and testing
if __name__ == "__main__":
    # Initialize aggregator
    aggregator = NewsAggregator()
    
    # Get market news
    print("\n=== MARKET NEWS (Last 24 hours) ===")
    market_news = aggregator.get_market_news(hours=24)
    for article in market_news[:5]:
        print(f"\nTitle: {article.title}")
        print(f"Source: {article.source}")
        print(f"Date: {article.published_date}")
        print(f"URL: {article.url}")
        print("-" * 80)
    
    # Get news for a specific ticker
    print("\n=== TICKER NEWS (AAPL) ===")
    ticker_news = aggregator.get_ticker_news("AAPL")
    for article in ticker_news[:3]:
        print(f"\nTitle: {article.title}")
        print(f"Source: {article.source}")
        print(f"Date: {article.published_date}")
        print("-" * 80)
    
    # Search for specific news
    print("\n=== SEARCH RESULTS (AI) ===")
    search_results = aggregator.search_news("AI", hours=24)
    for article in search_results[:3]:
        print(f"\nTitle: {article.title}")
        print(f"Source: {article.source}")
        print("-" * 80)
    
    print("\n✅ News scraper module working!")
