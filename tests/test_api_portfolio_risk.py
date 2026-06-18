"""Tests for the /api/portfolio/risk/{ticker} endpoint."""

from __future__ import annotations

from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    with (
        patch("api.main.StockMarketIntelligence"),
        patch("api.main.ComprehensiveSignalEngine"),
    ):
        from api.main import app

        return TestClient(app, raise_server_exceptions=False)


class TestPortfolioRiskEndpoint:
    def test_valid_ticker_returns_expected_keys(self, client):
        prices = pd.Series(100 * np.exp(np.cumsum(np.random.default_rng(7).normal(0, 0.01, 252))))
        mock_hist = pd.DataFrame({"Close": prices})

        with patch("yfinance.Ticker") as mock_yf:
            mock_yf.return_value.history.return_value = mock_hist
            resp = client.get("/api/portfolio/risk/AAPL")

        assert resp.status_code == 200
        body = resp.json()
        for key in ("ticker", "var_95", "sharpe_ratio", "max_drawdown", "annualised_vol", "timestamp"):
            assert key in body

    def test_invalid_ticker_returns_422(self, client):
        resp = client.get("/api/portfolio/risk/invalid!!")
        assert resp.status_code == 422

    def test_empty_history_returns_404(self, client):
        with patch("yfinance.Ticker") as mock_yf:
            mock_yf.return_value.history.return_value = pd.DataFrame()
            resp = client.get("/api/portfolio/risk/AAPL")
        assert resp.status_code == 404

    def test_ticker_label_in_response(self, client):
        prices = pd.Series(100 * np.exp(np.cumsum(np.random.default_rng(9).normal(0, 0.01, 252))))
        mock_hist = pd.DataFrame({"Close": prices})

        with patch("yfinance.Ticker") as mock_yf:
            mock_yf.return_value.history.return_value = mock_hist
            resp = client.get("/api/portfolio/risk/MSFT")

        assert resp.status_code == 200
        assert resp.json()["ticker"] == "MSFT"

    @pytest.mark.parametrize("period", ["3mo", "6mo", "1y"])
    def test_period_query_param_accepted(self, client, period):
        prices = pd.Series(100 * np.exp(np.cumsum(np.random.default_rng(11).normal(0, 0.01, 252))))
        mock_hist = pd.DataFrame({"Close": prices})

        with patch("yfinance.Ticker") as mock_yf:
            mock_yf.return_value.history.return_value = mock_hist
            resp = client.get(f"/api/portfolio/risk/GOOGL?period={period}")

        assert resp.status_code == 200
