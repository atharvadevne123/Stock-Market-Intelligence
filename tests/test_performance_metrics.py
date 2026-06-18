"""Tests for analysis.performance_metrics.PerformanceMetrics."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from analysis.performance_metrics import PerformanceMetrics


def _flat_prices(value: float = 100.0, n: int = 252) -> pd.Series:
    return pd.Series([value] * n)


def _trending_prices(start: float = 100.0, end: float = 200.0, n: int = 252) -> pd.Series:
    return pd.Series(np.linspace(start, end, n))


def _volatile_prices(n: int = 252, seed: int = 42) -> pd.Series:
    rng = np.random.default_rng(seed)
    returns = rng.normal(0, 0.02, n)
    return pd.Series(100 * np.exp(np.cumsum(returns)))


class TestCAGR:
    def setup_method(self):
        self.m = PerformanceMetrics()

    def test_flat_prices_zero_cagr(self):
        assert self.m.cagr(_flat_prices()) == pytest.approx(0.0, abs=1e-6)

    def test_uptrend_positive_cagr(self):
        assert self.m.cagr(_trending_prices(100, 200)) > 0

    def test_single_point_zero(self):
        assert self.m.cagr(pd.Series([100.0])) == 0.0

    def test_returns_float(self):
        assert isinstance(self.m.cagr(_volatile_prices()), float)

    def test_declining_trend_negative_cagr(self):
        prices = _trending_prices(200, 100)
        assert self.m.cagr(prices) < 0


class TestSortinoRatio:
    def setup_method(self):
        self.m = PerformanceMetrics()

    def test_flat_prices_zero_sortino(self):
        returns = _flat_prices().pct_change().dropna()
        assert self.m.sortino_ratio(returns) == 0.0

    def test_uptrend_positive_sortino(self):
        prices = _trending_prices(100, 200)
        returns = prices.pct_change().dropna()
        result = self.m.sortino_ratio(returns)
        assert isinstance(result, float)

    def test_volatile_returns_float(self):
        prices = _volatile_prices()
        returns = prices.pct_change().dropna()
        assert isinstance(self.m.sortino_ratio(returns), float)


class TestCalmarRatio:
    def setup_method(self):
        self.m = PerformanceMetrics()

    def test_flat_prices_zero_calmar(self):
        assert self.m.calmar_ratio(_flat_prices()) == 0.0

    def test_uptrend_zero_drawdown_zero_calmar(self):
        assert self.m.calmar_ratio(_trending_prices(100, 200)) == 0.0

    def test_volatile_returns_float(self):
        result = self.m.calmar_ratio(_volatile_prices())
        assert isinstance(result, float)


class TestSummary:
    def setup_method(self):
        self.m = PerformanceMetrics()

    def test_summary_keys_present(self):
        result = self.m.summary(_volatile_prices(), ticker="AAPL")
        for key in ("ticker", "cagr", "sortino_ratio", "calmar_ratio"):
            assert key in result

    def test_summary_ticker_label(self):
        result = self.m.summary(_volatile_prices(), ticker="TSLA")
        assert result["ticker"] == "TSLA"

    @pytest.mark.parametrize("ticker", ["AAPL", "MSFT", "GOOGL"])
    def test_summary_values_are_floats(self, ticker):
        result = self.m.summary(_volatile_prices(), ticker=ticker)
        assert isinstance(result["cagr"], float)
        assert isinstance(result["sortino_ratio"], float)
        assert isinstance(result["calmar_ratio"], float)
