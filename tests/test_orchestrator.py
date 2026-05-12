"""Tests for main_orchestrator module."""
from __future__ import annotations

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime


@pytest.fixture
def mock_components():
    news = MagicMock()
    news.get_ticker_news.return_value = []
    sentiment = MagicMock()
    sentiment.analyze_article.return_value = {
        "combined_sentiment": "positive",
        "combined_confidence": 0.85,
        "all_scores": {"positive": 0.85, "negative": 0.1, "neutral": 0.05},
    }
    signals = MagicMock()
    signals.generate_signal.return_value = {
        "ticker": "AAPL",
        "final_signal": "BUY",
        "combined_score": 0.4,
    }
    return news, sentiment, signals


@pytest.fixture
def orchestrator(mock_components):
    news, sentiment, signals = mock_components
    with (
        patch("main_orchestrator.NewsAggregator", return_value=news),
        patch("main_orchestrator.NewsArticleSentimentAnalyzer", return_value=sentiment),
        patch("main_orchestrator.ComprehensiveSignalEngine", return_value=signals),
    ):
        from main_orchestrator import StockMarketIntelligence
        orch = StockMarketIntelligence()
        orch.news_aggregator = news
        orch.sentiment_analyzer = sentiment
        orch.signal_engine = signals
        return orch


class TestStockMarketIntelligence:
    def test_init_succeeds(self, orchestrator):
        assert orchestrator is not None

    def test_analyze_ticker_returns_dict(self, orchestrator):
        result = orchestrator.analyze_ticker("AAPL")
        assert isinstance(result, dict)
        assert result.get("ticker") == "AAPL"

    def test_analyze_ticker_has_timestamp(self, orchestrator):
        result = orchestrator.analyze_ticker("AAPL")
        assert "timestamp" in result

    def test_analyze_ticker_calls_news(self, orchestrator, mock_components):
        news, _, _ = mock_components
        orchestrator.analyze_ticker("MSFT")
        news.get_ticker_news.assert_called_once_with("MSFT", hours=24)

    @pytest.mark.parametrize("ticker", ["AAPL", "MSFT", "GOOGL"])
    def test_analyze_various_tickers(self, orchestrator, ticker):
        orchestrator.news_aggregator.get_ticker_news.return_value = []
        result = orchestrator.analyze_ticker(ticker)
        assert result["ticker"] == ticker
