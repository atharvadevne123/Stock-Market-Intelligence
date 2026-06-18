"""Tests for utils.formatters."""

from __future__ import annotations

import pytest

from utils.formatters import format_currency, format_percentage, format_signal_label


class TestFormatCurrency:
    def test_positive_value(self):
        assert format_currency(1234.5) == "$1,234.50"

    def test_negative_value(self):
        assert format_currency(-99.9, symbol="£") == "-£99.90"

    def test_zero(self):
        assert format_currency(0) == "$0.00"

    def test_custom_symbol(self):
        result = format_currency(50.0, symbol="€")
        assert result.startswith("€")

    def test_custom_decimals(self):
        assert format_currency(1.0, decimals=0) == "$1"

    @pytest.mark.parametrize("value", [0.01, 100.0, 9999999.99])
    def test_always_returns_string(self, value):
        assert isinstance(format_currency(value), str)


class TestFormatPercentage:
    def test_multiply_mode(self):
        assert format_percentage(0.0523, multiply=True) == "5.23%"

    def test_direct_value(self):
        assert format_percentage(12.5) == "12.50%"

    def test_zero(self):
        assert format_percentage(0.0) == "0.00%"

    def test_custom_decimals(self):
        result = format_percentage(5.1234, decimals=1)
        assert result == "5.1%"

    @pytest.mark.parametrize("pct", [-5.0, 0.0, 50.0, 100.0])
    def test_returns_string_with_percent_sign(self, pct):
        result = format_percentage(pct)
        assert result.endswith("%")


class TestFormatSignalLabel:
    def test_strong_buy(self):
        assert format_signal_label("STRONG_BUY") == "Strong Buy"

    def test_hold(self):
        assert format_signal_label("hold") == "Hold"

    def test_strong_sell(self):
        assert format_signal_label("STRONG_SELL") == "Strong Sell"

    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("BUY", "Buy"),
            ("SELL", "Sell"),
            ("NEUTRAL", "Neutral"),
        ],
    )
    def test_various_signals(self, raw, expected):
        assert format_signal_label(raw) == expected
