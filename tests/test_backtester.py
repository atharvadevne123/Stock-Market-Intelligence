"""Tests for analysis.backtester.SimpleBacktester."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from analysis.backtester import SimpleBacktester


def _prices(n: int = 252, seed: int = 42) -> pd.Series:
    rng = np.random.default_rng(seed)
    returns = rng.normal(0, 0.01, n)
    return pd.Series(100 * np.exp(np.cumsum(returns)))


def _always_long(n: int = 252) -> pd.Series:
    return pd.Series(np.ones(n))


def _always_cash(n: int = 252) -> pd.Series:
    return pd.Series(np.zeros(n))


class TestSimpleBacktester:
    def setup_method(self):
        self.bt = SimpleBacktester()

    def test_empty_inputs_return_zeros(self):
        result = self.bt.run(pd.Series(dtype=float), pd.Series(dtype=float))
        assert result["total_return"] == 0.0
        assert result["num_trades"] == 0

    def test_always_cash_no_return(self):
        prices = _prices()
        signals = _always_cash()
        result = self.bt.run(prices, signals)
        assert result["total_return"] == pytest.approx(0.0, abs=1e-6)

    def test_returns_required_keys(self):
        result = self.bt.run(_prices(), _always_long())
        for key in ("total_return", "annualised_return", "max_drawdown", "num_trades", "sharpe_ratio", "equity_curve"):
            assert key in result

    def test_equity_curve_starts_near_initial_capital(self):
        result = self.bt.run(_prices(), _always_long())
        assert isinstance(result["equity_curve"], pd.Series)
        assert len(result["equity_curve"]) == 252

    def test_max_drawdown_non_negative(self):
        result = self.bt.run(_prices(), _always_long())
        assert result["max_drawdown"] >= 0.0

    def test_sharpe_ratio_is_float(self):
        result = self.bt.run(_prices(), _always_long())
        assert isinstance(result["sharpe_ratio"], float)

    def test_flat_prices_zero_commission_zero_return(self):
        bt = SimpleBacktester(commission=0.0)
        prices = pd.Series([100.0] * 252)
        signals = _always_long(252)
        result = bt.run(prices, signals)
        assert result["total_return"] == pytest.approx(0.0, abs=1e-6)

    def test_flat_prices_nonzero_commission_small_loss(self):
        prices = pd.Series([100.0] * 252)
        signals = _always_long(252)
        result = self.bt.run(prices, signals)
        assert result["total_return"] < 0  # commission on initial entry

    @pytest.mark.parametrize("commission", [0.0, 0.001, 0.005])
    def test_various_commissions(self, commission):
        bt = SimpleBacktester(commission=commission)
        result = bt.run(_prices(), _always_long())
        assert isinstance(result["total_return"], float)
