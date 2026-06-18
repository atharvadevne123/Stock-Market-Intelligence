"""Tests for analysis.portfolio_risk.PortfolioRiskCalculator."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from analysis.portfolio_risk import PortfolioRiskCalculator


def _flat_prices(value: float = 100.0, n: int = 252) -> pd.Series:
    """Return a flat price series (zero returns)."""
    return pd.Series([value] * n)


def _trending_prices(start: float = 100.0, end: float = 150.0, n: int = 252) -> pd.Series:
    """Return a linearly trending price series."""
    return pd.Series(np.linspace(start, end, n))


def _volatile_prices(n: int = 252, seed: int = 42) -> pd.Series:
    """Return a synthetic random-walk price series."""
    rng = np.random.default_rng(seed)
    returns = rng.normal(0, 0.02, n)
    prices = 100 * np.exp(np.cumsum(returns))
    return pd.Series(prices)


class TestHistoricalVaR:
    def setup_method(self):
        self.calc = PortfolioRiskCalculator()

    def test_empty_returns_zero(self):
        assert self.calc.historical_var(pd.Series(dtype=float)) == 0.0

    def test_returns_positive_float(self):
        prices = _volatile_prices()
        returns = prices.pct_change().dropna()
        var = self.calc.historical_var(returns)
        assert isinstance(var, float)
        assert var >= 0

    @pytest.mark.parametrize("confidence", [0.90, 0.95, 0.99])
    def test_higher_confidence_higher_var(self, confidence: float):
        prices = _volatile_prices()
        returns = prices.pct_change().dropna()
        var = self.calc.historical_var(returns, confidence=confidence)
        assert var >= 0

    def test_flat_prices_zero_var(self):
        prices = _flat_prices()
        returns = prices.pct_change().dropna()
        assert self.calc.historical_var(returns) == pytest.approx(0.0, abs=1e-10)


class TestSharpeRatio:
    def setup_method(self):
        self.calc = PortfolioRiskCalculator()

    def test_flat_prices_zero_sharpe(self):
        prices = _flat_prices()
        returns = prices.pct_change().dropna()
        assert self.calc.sharpe_ratio(returns) == pytest.approx(0.0, abs=1e-6)

    def test_uptrend_positive_sharpe(self):
        prices = _trending_prices(100, 200)
        returns = prices.pct_change().dropna()
        assert self.calc.sharpe_ratio(returns) > 0

    def test_returns_float(self):
        prices = _volatile_prices()
        returns = prices.pct_change().dropna()
        assert isinstance(self.calc.sharpe_ratio(returns), float)


class TestMaxDrawdown:
    def setup_method(self):
        self.calc = PortfolioRiskCalculator()

    def test_flat_prices_zero_drawdown(self):
        assert self.calc.max_drawdown(_flat_prices()) == pytest.approx(0.0, abs=1e-10)

    def test_uptrend_zero_drawdown(self):
        prices = _trending_prices(100, 200)
        assert self.calc.max_drawdown(prices) == pytest.approx(0.0, abs=1e-10)

    def test_empty_prices_zero(self):
        assert self.calc.max_drawdown(pd.Series(dtype=float)) == 0.0

    def test_returns_positive(self):
        prices = _volatile_prices()
        dd = self.calc.max_drawdown(prices)
        assert 0.0 <= dd <= 1.0


class TestPortfolioCorrelation:
    def setup_method(self):
        self.calc = PortfolioRiskCalculator()

    def test_self_correlation_is_one(self):
        prices = _volatile_prices()
        returns = prices.pct_change().dropna()
        df = pd.DataFrame({"A": returns, "B": returns})
        corr = self.calc.portfolio_correlation(df)
        assert corr.loc["A", "B"] == pytest.approx(1.0, abs=1e-10)

    def test_correlation_shape(self):
        tickers = ["AAPL", "MSFT", "GOOGL"]
        rng = np.random.default_rng(1)
        df = pd.DataFrame(rng.normal(0, 0.01, (252, 3)), columns=tickers)
        corr = self.calc.portfolio_correlation(df)
        assert corr.shape == (3, 3)


class TestSummary:
    def setup_method(self):
        self.calc = PortfolioRiskCalculator()

    def test_summary_keys(self):
        prices = _volatile_prices()
        result = self.calc.summary(prices, ticker="AAPL")
        for key in ("ticker", "var_95", "sharpe_ratio", "max_drawdown", "annualised_vol", "timestamp"):
            assert key in result

    def test_summary_ticker_label(self):
        prices = _volatile_prices()
        result = self.calc.summary(prices, ticker="TSLA")
        assert result["ticker"] == "TSLA"

    @pytest.mark.parametrize("ticker", ["AAPL", "MSFT", "GOOGL", "AMZN"])
    def test_summary_for_various_tickers(self, ticker: str):
        prices = _volatile_prices()
        result = self.calc.summary(prices, ticker=ticker)
        assert result["ticker"] == ticker
        assert isinstance(result["var_95"], float)
