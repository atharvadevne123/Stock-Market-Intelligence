"""Tests for scraper.news_scraper module."""

from __future__ import annotations

from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from scraper.news_scraper import NewsAggregator, NewsArticle, RSSFeedScraper


class TestNewsArticle:
    def setup_method(self):
        self.article = NewsArticle(
            title="Apple Beats Earnings",
            content="Strong Q4 results across all segments.",
            source="Reuters",
            url="https://example.com/apple",
            published_date=datetime(2024, 1, 15, 10, 30),
            ticker="AAPL",
        )

    def test_to_dict_title(self):
        assert self.article.to_dict()["title"] == "Apple Beats Earnings"

    def test_to_dict_source(self):
        assert self.article.to_dict()["source"] == "Reuters"

    def test_to_dict_ticker(self):
        assert self.article.to_dict()["ticker"] == "AAPL"

    def test_to_dict_published_date_is_string(self):
        assert isinstance(self.article.to_dict()["published_date"], str)

    def test_article_no_ticker(self):
        article = NewsArticle(
            title="Market Update",
            content="Mixed session.",
            source="CNBC",
            url="https://example.com/market",
            published_date=datetime.now(),
        )
        assert article.ticker is None

    @pytest.mark.parametrize("source", ["Reuters", "Bloomberg", "CNBC", "MarketWatch", "WSJ"])
    def test_various_sources(self, source):
        article = NewsArticle("T", "C", source, f"https://x.com/{source}", datetime.now())
        assert article.source == source

    @pytest.mark.parametrize("ticker", ["AAPL", "MSFT", "GOOGL", None])
    def test_optional_ticker(self, ticker):
        article = NewsArticle("T", "C", "S", "https://x.com/t", datetime.now(), ticker)
        assert article.ticker == ticker


class TestRSSFeedScraper:
    def test_has_feeds_defined(self):
        assert len(RSSFeedScraper.FEEDS) > 0

    def test_feeds_are_strings(self):
        for name, url in RSSFeedScraper.FEEDS.items():
            assert isinstance(name, str) and isinstance(url, str)

    def test_init_creates_session(self):
        scraper = RSSFeedScraper()
        assert scraper.session is not None

    def test_configurable_timeout(self):
        assert RSSFeedScraper(timeout=30).timeout == 30

    def test_default_timeout(self):
        assert RSSFeedScraper().timeout == 10


class TestNewsArticleUrlHash:
    def test_hash_is_16_chars(self):
        article = NewsArticle("T", "C", "S", "https://example.com/test", datetime.now())
        assert len(article.url_hash) == 16

    def test_same_url_same_hash(self):
        a1 = NewsArticle("T1", "C1", "S1", "https://example.com/same", datetime.now())
        a2 = NewsArticle("T2", "C2", "S2", "https://example.com/same", datetime.now())
        assert a1.url_hash == a2.url_hash

    def test_different_urls_different_hashes(self):
        a1 = NewsArticle("T", "C", "S", "https://example.com/a", datetime.now())
        a2 = NewsArticle("T", "C", "S", "https://example.com/b", datetime.now())
        assert a1.url_hash != a2.url_hash

    def test_case_insensitive_url(self):
        a1 = NewsArticle("T", "C", "S", "https://EXAMPLE.COM/test", datetime.now())
        a2 = NewsArticle("T", "C", "S", "https://example.com/test", datetime.now())
        assert a1.url_hash == a2.url_hash

    def test_hash_is_string(self):
        article = NewsArticle("T", "C", "S", "https://x.com/hash-test", datetime.now())
        assert isinstance(article.url_hash, str)


class TestNewsAggregator:
    @patch("scraper.news_scraper.WebScraper")
    @patch("scraper.news_scraper.RSSFeedScraper")
    def test_get_market_news_filters_by_time(self, mock_rss_cls, mock_web_cls):
        mock_rss = mock_rss_cls.return_value
        old_article = NewsArticle("Old", "Content", "Source", "https://x.com/old", datetime.now() - timedelta(hours=48))
        new_article = NewsArticle("New", "Content", "Source", "https://x.com/new", datetime.now() - timedelta(hours=1))
        mock_rss.fetch_all_feeds.return_value = [old_article, new_article]
        aggregator = NewsAggregator()
        result = aggregator.get_market_news(hours=24)
        assert len(result) == 1
        assert result[0].title == "New"

    @patch("scraper.news_scraper.WebScraper")
    @patch("scraper.news_scraper.RSSFeedScraper")
    def test_search_news_filters_by_query(self, mock_rss_cls, mock_web_cls):
        mock_rss = mock_rss_cls.return_value
        ai_article = NewsArticle(
            "AI breakthroughs", "Content", "S", "https://x.com/ai", datetime.now() - timedelta(hours=1)
        )
        other_article = NewsArticle(
            "Oil prices rise", "Content", "S", "https://x.com/oil", datetime.now() - timedelta(hours=2)
        )
        mock_rss.fetch_all_feeds.return_value = [ai_article, other_article]
        aggregator = NewsAggregator()
        result = aggregator.search_news("AI", hours=24)
        assert len(result) == 1
        assert "AI" in result[0].title
