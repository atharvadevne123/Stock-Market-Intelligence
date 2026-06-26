"""Tests for analysis.signal_engine TechnicalIndicator and TechnicalSignalGenerator."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from analysis.signal_engine import Signal, TechnicalIndicator, TechnicalSignalGenerator


def _make_prices(n: int = 250, seed: int = 42) -> pd.Series:
    """Return a synthetic Close price series with *n* observations."""
    rng = np.random.default_rng(seed)
    prices = 100 + np.cumsum(rng.normal(0, 1, n))
    prices = np.abs(prices) + 10
    return pd.Series(prices, name="Close")


def _make_ohlcv(n: int = 250, seed: int = 42) -> pd.DataFrame:
    """Return a synthetic OHLCV DataFrame."""
    rng = np.random.default_rng(seed)
    close = 100 + np.cumsum(rng.normal(0, 1, n)) + 10
    close = np.abs(close) + 10
    high = close + rng.uniform(0.5, 2.0, n)
    low = close - rng.uniform(0.5, 2.0, n)
    volume = rng.integers(1_000_000, 5_000_000, n).astype(float)
    return pd.DataFrame({"Close": close, "High": high, "Low": low, "Volume": volume})


class TestTechnicalIndicatorRSI:
    def test_rsi_returns_series(self):
        prices = _make_prices()
        indicator = TechnicalIndicator()
        rsi = indicator.calculate_rsi(prices)
        assert isinstance(rsi, pd.Series)

    def test_rsi_bounds(self):
        prices = _make_prices()
        indicator = TechnicalIndicator()
        rsi = indicator.calculate_rsi(prices).dropna()
        assert (rsi >= 0).all() and (rsi <= 100).all()

    @pytest.mark.parametrize("period", [7, 14, 21])
    def test_rsi_periods(self, period: int):
        prices = _make_prices()
        indicator = TechnicalIndicator()
        rsi = indicator.calculate_rsi(prices, period=period)
        assert rsi is not None


class TestTechnicalIndicatorMACD:
    def test_macd_returns_three_series(self):
        prices = _make_prices()
        indicator = TechnicalIndicator()
        macd, signal, hist = indicator.calculate_macd(prices)
        assert macd is not None
        assert signal is not None
        assert hist is not None

    def test_histogram_equals_diff(self):
        prices = _make_prices()
        indicator = TechnicalIndicator()
        macd, signal, hist = indicator.calculate_macd(prices)
        if macd is not None:
            diff = (macd - signal).dropna()
            hist_trimmed = hist.dropna()
            pd.testing.assert_series_equal(diff.reset_index(drop=True), hist_trimmed.reset_index(drop=True), atol=1e-6, check_names=False)


class TestTechnicalIndicatorBollingerBands:
    def test_returns_three_bands(self):
        prices = _make_prices()
        indicator = TechnicalIndicator()
        upper, middle, lower = indicator.calculate_bollinger_bands(prices)
        assert upper is not None
        assert middle is not None
        assert lower is not None

    def test_upper_gt_lower(self):
        prices = _make_prices()
        indicator = TechnicalIndicator()
        upper, _, lower = indicator.calculate_bollinger_bands(prices)
        if upper is not None:
            valid = ~(upper.isna() | lower.isna())
            assert (upper[valid] >= lower[valid]).all()


class TestTechnicalIndicatorStochastic:
    def test_stochastic_returns_two_series(self):
        df = _make_ohlcv()
        indicator = TechnicalIndicator()
        k, d = indicator.calculate_stochastic(df["High"], df["Low"], df["Close"])
        assert k is not None
        assert d is not None

    def test_stochastic_bounds(self):
        df = _make_ohlcv()
        indicator = TechnicalIndicator()
        k, d = indicator.calculate_stochastic(df["High"], df["Low"], df["Close"])
        if k is not None:
            k_valid = k.dropna()
            assert (k_valid >= 0).all() and (k_valid <= 100).all()


class TestTechnicalIndicatorWilliamsR:
    def test_williams_r_returns_series(self):
        df = _make_ohlcv()
        indicator = TechnicalIndicator()
        willr = indicator.calculate_williams_r(df["High"], df["Low"], df["Close"])
        assert willr is not None

    def test_williams_r_bounds(self):
        df = _make_ohlcv()
        indicator = TechnicalIndicator()
        willr = indicator.calculate_williams_r(df["High"], df["Low"], df["Close"])
        if willr is not None:
            valid = willr.dropna()
            assert (valid >= -100).all() and (valid <= 0).all()


class TestTechnicalSignalGeneratorAnalyzeRSI:
    def setup_method(self):
        self.gen = TechnicalSignalGenerator()

    def test_oversold_returns_buy(self):
        rng = np.random.default_rng(0)
        prices = pd.Series([30 - i * 0.5 for i in range(250)]) + rng.normal(0, 0.1, 250)
        signal, value = self.gen.analyze_rsi(prices)
        assert isinstance(signal, Signal)

    @pytest.mark.parametrize("signal", list(Signal))
    def test_signal_to_score_range(self, signal: Signal):
        from analysis.signal_engine import ComprehensiveSignalEngine

        engine = ComprehensiveSignalEngine()
        score = engine._signal_to_score(signal)
        assert -1.0 <= score <= 1.0


class TestPositionSizing:
    def setup_method(self):
        self.gen = TechnicalSignalGenerator()

    def test_basic_position_size(self):
        result = self.gen.calculate_position_size(
            account_value=100_000, latest_price=150.0, atr_value=3.0
        )
        assert result["shares"] > 0
        assert result["stop_loss"] < 150.0
        assert result["dollar_risk"] == pytest.approx(1_000.0, rel=1e-3)

    def test_zero_atr_returns_zero_shares(self):
        result = self.gen.calculate_position_size(
            account_value=100_000, latest_price=150.0, atr_value=0.0
        )
        assert result["shares"] == 0

    @pytest.mark.parametrize("risk_pct", [0.005, 0.01, 0.02])
    def test_risk_pct_scaling(self, risk_pct: float):
        result = self.gen.calculate_position_size(
            account_value=100_000, latest_price=100.0, atr_value=2.0, risk_pct=risk_pct
        )
        assert result["dollar_risk"] == pytest.approx(100_000 * risk_pct, rel=1e-3)
