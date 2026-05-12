"""Tests for api.main FastAPI application."""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from fastapi.testclient import TestClient


@pytest.fixture
def mock_system():
    system = MagicMock()
    system.analyze_ticker.return_value = {
        "ticker": "AAPL",
        "signal": "BUY",
        "timestamp": "2024-01-01T00:00:00",
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
    }
    engine.technical_generator.generate_technical_signal.return_value = {
        "ticker": "AAPL",
        "signal": "HOLD",
        "latest_price": 175.0,
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
        resp = client.get("/")
        assert resp.status_code == 200

    def test_root_has_name(self, client):
        resp = client.get("/")
        assert "name" in resp.json()

    def test_root_has_status(self, client):
        resp = client.get("/")
        assert resp.json()["status"] == "running"


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200

    def test_health_status_healthy(self, client):
        resp = client.get("/health")
        assert resp.json()["status"] == "healthy"

    def test_health_has_timestamp(self, client):
        resp = client.get("/health")
        assert "timestamp" in resp.json()


class TestAnalyzeEndpoint:
    def test_analyze_aapl(self, client, mock_system):
        resp = client.get("/api/analyze/AAPL")
        assert resp.status_code == 200
        mock_system.analyze_ticker.assert_called_once_with("AAPL", hours=24)

    def test_analyze_custom_hours(self, client, mock_system):
        resp = client.get("/api/analyze/MSFT?hours=48")
        assert resp.status_code == 200
        mock_system.analyze_ticker.assert_called_once_with("MSFT", hours=48)

    @pytest.mark.parametrize("ticker", ["AAPL", "MSFT", "GOOGL", "TSLA"])
    def test_analyze_various_tickers(self, client, ticker):
        resp = client.get(f"/api/analyze/{ticker}")
        assert resp.status_code == 200


class TestSignalEndpoint:
    def test_signal_returns_200(self, client):
        resp = client.get("/api/signals/AAPL")
        assert resp.status_code == 200

    def test_signal_has_final_signal(self, client):
        resp = client.get("/api/signals/AAPL")
        assert "final_signal" in resp.json()


class TestTechnicalEndpoint:
    def test_technical_returns_200(self, client):
        resp = client.get("/api/technical/AAPL")
        assert resp.status_code == 200

    def test_technical_has_signal(self, client):
        resp = client.get("/api/technical/AAPL")
        assert "signal" in resp.json()
