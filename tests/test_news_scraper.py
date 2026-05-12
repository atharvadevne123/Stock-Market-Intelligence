"""Tests for scraper.news_scraper module."""
from __future__ import annotations

import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from scraper.news_scraper import NewsArticle, NewsAggregator, RSSFeedScraper


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

    def test_to_dict_has_title(self):
        d = self.article.to_dict()
        assert d["title"] == "Apple Beats Earnings"

    def test_to_dict_has_content(self):
        d = self.article.to_dict()
        assert d["content"] == "Strong Q4 results across all segments."

    def test_to_dict_has_source(self):
        d = self.article.to_dict()
        assert d["source"] == "Reuters"

    def test_to_dict_has_url(self):
        d = self.article.to_dict()
        assert "url" in d

    def test_to_dict_has_ticker(self):
        d = self.article.to_dict()
        assert d["ticker"] == "AAPL"

    def test_to_dict_published_date_is_string(self):
        d = self.article.to_dict()
        assert isinstance(d["published_date"], str)

    def test_article_no_ticker(self):
        article = NewsArticle(
            title="Market Update",
            content="Markets closed mixed.",
            source="CNBC",
            url="https://example.com/market",
            published_date=datetime.now(),
        )
        assert article.ticker is None
        d = article.to_dict()
        assert d["ticker"] is None

    @pytest.mark.parametrize("source", ["Reuters", "Bloomberg", "CNBC", "MarketWatch"])
    def test_various_sources(self, source):
        article = NewsArticle(
            title="Test",
            content="Test content",
            source=source,
            url=f"https://example.com/{source.lower()}",
            published_date=datetime.now(),
        )
        assert article.source == source


class TestRSSFeedScraper:
    def test_has_feeds_defined(self):
        assert len(RSSFeedScraper.FEEDS) > 0

    def test_feeds_are_strings(self):
        for name, url in RSSFeedScraper.FEEDS.items():
            assert isinstance(name, str)
            assert isinstance(url, str)

    def test_init_creates_session(self):
        scraper = RSSFeedScraper()
        assert scraper.session is not None

    def test_timeout_configurable(self):
        scraper = RSSFeedScraper(timeout=30)
        assert scraper.timeout == 30


class TestNewsAggregator:
    @patch("scraper.news_scraper.RSSFeedScraper")
    @patch("scraper.news_scraper.WebScraper")
    def test_init_creates_scrapers(self, mock_web, mock_rss):
        aggregator = NewsAggregator()
        assert aggregator.rss_scraper is not None
        assert aggregator.web_scraper is not None

    @patch("scraper.news_scraper.RSSFeedScraper")
    @patch("scraper.news_scraper.WebScraper")
    def test_get_market_news_calls_rss(self, mock_web_cls, mock_rss_cls):
        mock_rss = mock_rss_cls.return_value
        mock_rss.fetch_all_feeds.return_value = []
        aggregator = NewsAggregator()
        result = aggregator.get_market_news(hours=24)
        mock_rss.fetch_all_feeds.assert_called_once()
        assert isinstance(result, list)
