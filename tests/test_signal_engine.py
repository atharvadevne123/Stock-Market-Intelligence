"""Tests for analysis.signal_engine module."""
from __future__ import annotations

import pytest
from unittest.mock import patch, MagicMock
from analysis.signal_engine import (
    Signal,
    TechnicalIndicator,
    SentimentSignalGenerator,
    ComprehensiveSignalEngine,
)


class TestSignalEnum:
    def test_buy_value(self):
        assert Signal.BUY.value == "BUY"

    def test_sell_value(self):
        assert Signal.SELL.value == "SELL"

    def test_hold_value(self):
        assert Signal.HOLD.value == "HOLD"

    def test_strong_buy_value(self):
        assert Signal.STRONG_BUY.value == "STRONG_BUY"

    def test_strong_sell_value(self):
        assert Signal.STRONG_SELL.value == "STRONG_SELL"

    def test_all_signals_defined(self):
        assert len(Signal) == 5

    @pytest.mark.parametrize("signal", list(Signal))
    def test_signal_has_string_value(self, signal):
        assert isinstance(signal.value, str)


class TestSentimentSignalGenerator:
    def setup_method(self):
        self.generator = SentimentSignalGenerator()

    def test_empty_scores_returns_hold(self):
        assert self.generator.generate_sentiment_signal([]) == Signal.HOLD

    def test_all_positive_returns_strong_buy(self):
        scores = [{"combined_sentiment": "positive"}] * 10
        assert self.generator.generate_sentiment_signal(scores) == Signal.STRONG_BUY

    def test_all_negative_returns_strong_sell(self):
        scores = [{"combined_sentiment": "negative"}] * 10
        assert self.generator.generate_sentiment_signal(scores) == Signal.STRONG_SELL

    def test_all_neutral_returns_hold(self):
        scores = [{"combined_sentiment": "neutral"}] * 10
        assert self.generator.generate_sentiment_signal(scores) == Signal.HOLD

    def test_mixed_balanced_returns_hold(self):
        scores = (
            [{"combined_sentiment": "positive"}] * 3
            + [{"combined_sentiment": "negative"}] * 3
            + [{"combined_sentiment": "neutral"}] * 4
        )
        assert self.generator.generate_sentiment_signal(scores) == Signal.HOLD

    @pytest.mark.parametrize("positive_pct,expected", [
        (0.7, Signal.STRONG_BUY),
        (0.5, Signal.BUY),
        (0.1, Signal.HOLD),
    ])
    def test_positive_ratios(self, positive_pct, expected):
        total = 10
        pos = int(total * positive_pct)
        neg = total - pos
        scores = (
            [{"combined_sentiment": "positive"}] * pos
            + [{"combined_sentiment": "negative"}] * neg
        )
        assert self.generator.generate_sentiment_signal(scores) == expected

    @pytest.mark.parametrize("negative_pct,expected", [
        (0.7, Signal.STRONG_SELL),
        (0.5, Signal.SELL),
    ])
    def test_negative_ratios(self, negative_pct, expected):
        total = 10
        neg = int(total * negative_pct)
        pos = total - neg
        scores = (
            [{"combined_sentiment": "negative"}] * neg
            + [{"combined_sentiment": "positive"}] * pos
        )
        assert self.generator.generate_sentiment_signal(scores) == expected

    def test_single_positive_score(self):
        scores = [{"combined_sentiment": "positive"}]
        result = self.generator.generate_sentiment_signal(scores)
        assert result in (Signal.BUY, Signal.STRONG_BUY, Signal.HOLD)

    def test_missing_combined_sentiment_key(self):
        scores = [{"other_key": "positive"}] * 5
        result = self.generator.generate_sentiment_signal(scores)
        assert result == Signal.HOLD


class TestComprehensiveSignalEngineScoring:
    def setup_method(self):
        self.engine = ComprehensiveSignalEngine()

    @pytest.mark.parametrize("signal,expected_score", [
        (Signal.STRONG_BUY, 1.0),
        (Signal.BUY, 0.5),
        (Signal.HOLD, 0.0),
        (Signal.SELL, -0.5),
        (Signal.STRONG_SELL, -1.0),
    ])
    def test_signal_to_score(self, signal, expected_score):
        assert self.engine._signal_to_score(signal) == expected_score

    def test_signal_to_score_is_cached(self):
        score1 = self.engine._signal_to_score(Signal.BUY)
        score2 = self.engine._signal_to_score(Signal.BUY)
        assert score1 == score2 == 0.5

    def test_generate_signal_no_sentiment(self, mock_yf_download):
        result = self.engine.generate_signal("AAPL")
        assert "ticker" in result
        assert result["ticker"] == "AAPL"
        assert "final_signal" in result
        assert result["final_signal"] in [s.value for s in Signal]

    def test_generate_signal_with_positive_sentiment(self, mock_yf_download, sample_sentiment_scores):
        result = self.engine.generate_signal("AAPL", sentiment_scores=sample_sentiment_scores)
        assert result["sentiment"]["articles_analyzed"] == 3
        assert result["final_signal"] in [s.value for s in Signal]

    def test_generate_signal_custom_weights(self, mock_yf_download):
        weights = {"technical": 0.5, "sentiment": 0.5}
        result = self.engine.generate_signal("AAPL", weights=weights)
        assert result["weights"] == weights

    def test_generate_signal_has_timestamp(self, mock_yf_download):
        result = self.engine.generate_signal("AAPL")
        assert "timestamp" in result

    def test_generate_signal_has_combined_score(self, mock_yf_download):
        result = self.engine.generate_signal("AAPL")
        assert "combined_score" in result
        assert isinstance(result["combined_score"], float)

    @pytest.mark.parametrize("ticker", ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"])
    def test_generate_signal_for_various_tickers(self, mock_yf_download, ticker):
        result = self.engine.generate_signal(ticker)
        assert result["ticker"] == ticker
