"""Tests for api.main FastAPI application."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def mock_system():
    system = MagicMock()
    system.analyze_ticker.return_value = {
        "ticker": "AAPL",
        "signal": "BUY",
        "timestamp": "2024-01-01T00:00:00",
        "analysis_steps": [],
    }
    system.analyze_portfolio.return_value = {"tickers": ["AAPL"], "signals": []}
    system.get_market_overview.return_value = {"status": "active", "tickers": []}
    return system


@pytest.fixture
def mock_signal_engine():
    engine = MagicMock()
    engine.generate_signal.return_value = {
        "ticker": "AAPL",
        "final_signal": "BUY",
        "combined_score": 0.5,
        "timestamp": "2024-01-01T00:00:00",
    }
    engine.technical_generator.generate_technical_signal.return_value = {
        "ticker": "AAPL",
        "signal": "HOLD",
        "latest_price": 175.0,
        "confidence": 0.5,
    }
    return engine


@pytest.fixture
def client(mock_system, mock_signal_engine):
    with (
        patch("api.main.StockMarketIntelligence", return_value=mock_system),
        patch("api.main.ComprehensiveSignalEngine", return_value=mock_signal_engine),
        patch("api.main.NewsAggregator", return_value=MagicMock()),
        patch("api.main.NewsArticleSentimentAnalyzer", return_value=MagicMock()),
    ):
        from api.main import app
        with TestClient(app) as c:
            yield c


class TestRootEndpoint:
    def test_root_returns_200(self, client):
        assert client.get("/").status_code == 200

    def test_root_has_name(self, client):
        assert "name" in client.get("/").json()

    def test_root_status_running(self, client):
        assert client.get("/").json()["status"] == "running"


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        assert client.get("/health").status_code == 200

    def test_health_status_healthy(self, client):
        assert client.get("/health").json()["status"] == "healthy"

    def test_health_has_timestamp(self, client):
        assert "timestamp" in client.get("/health").json()


class TestVersionEndpoint:
    def test_version_returns_200(self, client):
        assert client.get("/api/version").status_code == 200

    def test_version_has_version_field(self, client):
        assert "version" in client.get("/api/version").json()

    def test_version_has_uptime(self, client):
        assert "uptime_seconds" in client.get("/api/version").json()


class TestMetricsEndpoint:
    def test_metrics_returns_200(self, client):
        assert client.get("/api/metrics").status_code == 200

    def test_metrics_has_requests_total(self, client):
        assert "requests_total" in client.get("/api/metrics").json()

    def test_metrics_has_errors_total(self, client):
        assert "errors_total" in client.get("/api/metrics").json()


class TestAnalyzeEndpoint:
    def test_analyze_returns_200(self, client):
        assert client.get("/api/analyze/AAPL").status_code == 200

    def test_analyze_calls_system(self, client, mock_system):
        client.get("/api/analyze/AAPL")
        mock_system.analyze_ticker.assert_called()

    def test_analyze_custom_hours(self, client, mock_system):
        client.get("/api/analyze/MSFT?hours=48")
        mock_system.analyze_ticker.assert_called_with("MSFT", hours=48)

    @pytest.mark.parametrize("ticker", ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"])
    def test_analyze_various_tickers(self, client, ticker):
        assert client.get(f"/api/analyze/{ticker}").status_code == 200

    def test_analyze_system_error_returns_500(self, client, mock_system):
        mock_system.analyze_ticker.side_effect = RuntimeError("DB down")
        resp = client.get("/api/analyze/AAPL")
        assert resp.status_code == 500


class TestSignalEndpoint:
    def test_signal_returns_200(self, client):
        assert client.get("/api/signals/AAPL").status_code == 200

    def test_signal_has_final_signal(self, client):
        assert "final_signal" in client.get("/api/signals/AAPL").json()

    def test_signal_engine_error_returns_500(self, client, mock_signal_engine):
        mock_signal_engine.generate_signal.side_effect = RuntimeError("Engine failed")
        assert client.get("/api/signals/AAPL").status_code == 500


class TestTechnicalEndpoint:
    def test_technical_returns_200(self, client):
        assert client.get("/api/technical/AAPL").status_code == 200

    def test_technical_has_signal(self, client):
        assert "signal" in client.get("/api/technical/AAPL").json()


class TestPortfolioEndpoint:
    def test_portfolio_returns_200(self, client):
        resp = client.get("/api/portfolio?tickers=AAPL,MSFT")
        assert resp.status_code == 200

    def test_portfolio_no_tickers_returns_422(self, client):
        resp = client.get("/api/portfolio")
        assert resp.status_code == 422
