"""Tests for main_orchestrator module."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_news():
    news = MagicMock()
    news.get_ticker_news.return_value = []
    news.get_market_news.return_value = []
    return news


@pytest.fixture
def mock_sentiment():
    sentiment = MagicMock()
    sentiment.analyze_article.return_value = {
        "combined_sentiment": "positive",
        "combined_confidence": 0.85,
        "all_scores": {"positive": 0.85, "negative": 0.1, "neutral": 0.05},
    }
    return sentiment


@pytest.fixture
def mock_signals():
    signals = MagicMock()
    signals.generate_signal.return_value = {
        "ticker": "AAPL",
        "final_signal": "BUY",
        "combined_score": 0.4,
    }
    return signals


@pytest.fixture
def orchestrator(mock_news, mock_sentiment, mock_signals):
    with (
        patch("main_orchestrator.NewsAggregator", return_value=mock_news),
        patch("main_orchestrator.NewsArticleSentimentAnalyzer", return_value=mock_sentiment),
        patch("main_orchestrator.ComprehensiveSignalEngine", return_value=mock_signals),
    ):
        from main_orchestrator import StockMarketIntelligence

        orch = StockMarketIntelligence()
        orch.news_aggregator = mock_news
        orch.sentiment_analyzer = mock_sentiment
        orch.signal_engine = mock_signals
        return orch


class TestAnalyzeTicker:
    def test_returns_dict(self, orchestrator):
        assert isinstance(orchestrator.analyze_ticker("AAPL"), dict)

    def test_has_ticker(self, orchestrator):
        assert orchestrator.analyze_ticker("AAPL")["ticker"] == "AAPL"

    def test_has_timestamp(self, orchestrator):
        assert "timestamp" in orchestrator.analyze_ticker("AAPL")

    def test_calls_news_aggregator(self, orchestrator, mock_news):
        orchestrator.analyze_ticker("MSFT")
        mock_news.get_ticker_news.assert_called_once_with("MSFT", hours=24)

    def test_custom_hours(self, orchestrator, mock_news):
        orchestrator.analyze_ticker("AAPL", hours=48)
        mock_news.get_ticker_news.assert_called_once_with("AAPL", hours=48)

    @pytest.mark.parametrize("ticker", ["AAPL", "MSFT", "GOOGL", "TSLA"])
    def test_various_tickers(self, orchestrator, ticker):
        orchestrator.news_aggregator.get_ticker_news.return_value = []
        result = orchestrator.analyze_ticker(ticker)
        assert result["ticker"] == ticker


class TestAnalyzePortfolio:
    def test_returns_dict(self, orchestrator):
        result = orchestrator.analyze_portfolio(["AAPL", "MSFT"])
        assert isinstance(result, dict)

    def test_has_portfolio(self, orchestrator):
        result = orchestrator.analyze_portfolio(["AAPL", "MSFT"])
        assert result["portfolio"] == ["AAPL", "MSFT"]

    def test_has_summary(self, orchestrator):
        result = orchestrator.analyze_portfolio(["AAPL"])
        assert "summary" in result

    def test_summary_has_recommendation(self, orchestrator):
        result = orchestrator.analyze_portfolio(["AAPL"])
        assert "recommendation" in result["summary"]

    def test_summary_recommendation_valid(self, orchestrator):
        result = orchestrator.analyze_portfolio(["AAPL"])
        assert result["summary"]["recommendation"] in ("BULLISH", "BEARISH", "NEUTRAL")


class TestGetMarketOverview:
    def test_returns_dict(self, orchestrator):
        result = orchestrator.get_market_overview()
        assert isinstance(result, dict)

    def test_has_market_sentiment(self, orchestrator):
        result = orchestrator.get_market_overview()
        assert "market_sentiment" in result

    def test_market_sentiment_valid(self, orchestrator):
        result = orchestrator.get_market_overview()
        assert result["market_sentiment"] in ("BULLISH", "BEARISH", "NEUTRAL")


class TestPortfolioSummary:
    def test_bullish_recommendation(self, orchestrator):
        analyses = [
            {"signal": {"final_signal": "BUY"}},
            {"signal": {"final_signal": "BUY"}},
            {"signal": {"final_signal": "STRONG_BUY"}},
        ]
        summary = orchestrator._generate_portfolio_summary(analyses)
        assert summary["recommendation"] == "BULLISH"

    def test_bearish_recommendation(self, orchestrator):
        analyses = [
            {"signal": {"final_signal": "SELL"}},
            {"signal": {"final_signal": "SELL"}},
            {"signal": {"final_signal": "STRONG_SELL"}},
        ]
        summary = orchestrator._generate_portfolio_summary(analyses)
        assert summary["recommendation"] == "BEARISH"

    def test_neutral_recommendation(self, orchestrator):
        analyses = [
            {"signal": {"final_signal": "BUY"}},
            {"signal": {"final_signal": "SELL"}},
        ]
        summary = orchestrator._generate_portfolio_summary(analyses)
        assert summary["recommendation"] == "NEUTRAL"

    def test_empty_analyses_returns_neutral(self, orchestrator):
        summary = orchestrator._generate_portfolio_summary([])
        assert summary["recommendation"] == "NEUTRAL"

    def test_summary_has_total_tickers(self, orchestrator):
        analyses = [{"signal": {"final_signal": "BUY"}}] * 3
        summary = orchestrator._generate_portfolio_summary(analyses)
        assert summary.get("total_tickers") == 3

    @pytest.mark.parametrize("signal,expected", [
        ("STRONG_BUY", "BULLISH"),
        ("STRONG_SELL", "BEARISH"),
        ("HOLD", "NEUTRAL"),
    ])
    def test_single_signal_recommendation(self, orchestrator, signal: str, expected: str):
        analyses = [{"signal": {"final_signal": signal}}]
        summary = orchestrator._generate_portfolio_summary(analyses)
        assert summary["recommendation"] == expected


class TestAnalyzeTickerEdgeCases:
    def test_analyze_ticker_returns_ticker_field(self, orchestrator):
        result = orchestrator.analyze_ticker("AAPL")
        assert result["ticker"] == "AAPL"

    def test_analyze_ticker_with_large_hours(self, orchestrator):
        result = orchestrator.analyze_ticker("MSFT", hours=720)
        assert isinstance(result, dict)

    def test_analyze_ticker_no_articles(self, orchestrator):
        orchestrator.news_aggregator.get_ticker_news.return_value = []
        result = orchestrator.analyze_ticker("AAPL")
        assert result["news"]["articles_found"] == 0
