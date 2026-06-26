"""Signal engine combining technical indicators and sentiment for BUY/SELL/HOLD signals."""

from __future__ import annotations

import logging
from datetime import datetime
from enum import Enum
from functools import lru_cache
from typing import Optional

import pandas as pd
import yfinance as yf

try:
    import pandas_ta as ta
except ImportError:
    import pandas_ta_classic as ta

logger = logging.getLogger(__name__)


class Signal(Enum):
    """Trading signal categories."""

    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    STRONG_BUY = "STRONG_BUY"
    STRONG_SELL = "STRONG_SELL"


class TechnicalIndicator:
    """Calculate common technical indicators using pandas-ta."""

    @staticmethod
    def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
        """Return the Relative Strength Index series."""
        return ta.rsi(prices, length=period)

    @staticmethod
    def calculate_macd(
        prices: pd.Series,
    ) -> tuple[pd.Series | None, pd.Series | None, pd.Series | None]:
        """Return (MACD line, signal line, histogram) or (None, None, None) on failure."""
        macd_result = ta.macd(prices)
        if macd_result is not None and len(macd_result.columns) >= 3:
            return (
                macd_result.iloc[:, 0],
                macd_result.iloc[:, 1],
                macd_result.iloc[:, 2],
            )
        return None, None, None

    @staticmethod
    def calculate_bollinger_bands(
        prices: pd.Series, period: int = 20
    ) -> tuple[pd.Series | None, pd.Series | None, pd.Series | None]:
        """Return (upper, middle, lower) Bollinger Band series."""
        bb = ta.bbands(prices, length=period)
        if bb is not None and len(bb.columns) >= 3:
            cols = bb.columns.tolist()
            upper_col = next((c for c in cols if c.startswith("BBU_")), cols[2])
            mid_col = next((c for c in cols if c.startswith("BBM_")), cols[1])
            lower_col = next((c for c in cols if c.startswith("BBL_")), cols[0])
            return bb[upper_col], bb[mid_col], bb[lower_col]
        return None, None, None

    @staticmethod
    def calculate_moving_averages(
        prices: pd.Series,
    ) -> tuple[pd.Series, pd.Series]:
        """Return (50-day SMA, 200-day SMA)."""
        return ta.sma(prices, length=50), ta.sma(prices, length=200)

    @staticmethod
    def calculate_atr(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        period: int = 14,
    ) -> pd.Series:
        """Return the Average True Range series."""
        return ta.atr(high, low, close, length=period)

    @staticmethod
    def calculate_stochastic(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        k_period: int = 14,
        d_period: int = 3,
    ) -> tuple[pd.Series | None, pd.Series | None]:
        """Return (%K, %D) stochastic oscillator series."""
        stoch = ta.stoch(high, low, close, k=k_period, d=d_period)
        if stoch is not None and len(stoch.columns) >= 2:
            return stoch.iloc[:, 0], stoch.iloc[:, 1]
        return None, None

    @staticmethod
    def calculate_williams_r(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        period: int = 14,
    ) -> pd.Series | None:
        """Return Williams %R series (range -100 to 0)."""
        return ta.willr(high, low, close, length=period)


class TechnicalSignalGenerator:
    """Generate buy/sell/hold signals from technical indicators."""

    def __init__(self) -> None:
        self.indicators = TechnicalIndicator()

    def analyze_rsi(self, prices: pd.Series) -> tuple[Signal, float]:
        """Generate RSI-based signal."""
        rsi = self.indicators.calculate_rsi(prices)
        latest_rsi = float(rsi.iloc[-1])
        if latest_rsi > 70:
            return Signal.SELL, latest_rsi
        if latest_rsi < 30:
            return Signal.BUY, latest_rsi
        return Signal.HOLD, latest_rsi

    def analyze_macd(self, prices: pd.Series) -> tuple[Signal, dict]:
        """Generate MACD-based signal."""
        macd_line, signal_line, histogram = self.indicators.calculate_macd(prices)
        if macd_line is None:
            return Signal.HOLD, {}

        latest_macd = float(macd_line.iloc[-1])
        latest_signal = float(signal_line.iloc[-1])
        latest_hist = float(histogram.iloc[-1])
        prev_hist = float(histogram.iloc[-2])

        result = {
            "macd": latest_macd,
            "signal": latest_signal,
            "histogram": latest_hist,
        }
        if latest_macd > latest_signal and latest_hist > prev_hist:
            return Signal.BUY, result
        if latest_macd < latest_signal and latest_hist < prev_hist:
            return Signal.SELL, result
        return Signal.HOLD, result

    def analyze_moving_averages(self, prices: pd.Series) -> tuple[Signal, dict]:
        """Generate moving-average crossover signal."""
        ma50, ma200 = self.indicators.calculate_moving_averages(prices)
        latest_price = float(prices.iloc[-1])
        latest_ma50 = float(ma50.iloc[-1])
        latest_ma200 = float(ma200.iloc[-1])
        result = {"price": latest_price, "ma50": latest_ma50, "ma200": latest_ma200}
        if latest_ma50 > latest_ma200 and latest_price > latest_ma50:
            return Signal.BUY, result
        if latest_ma50 < latest_ma200 and latest_price < latest_ma50:
            return Signal.SELL, result
        return Signal.HOLD, result

    def analyze_stochastic(
        self,
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
    ) -> tuple[Signal, dict]:
        """Generate stochastic oscillator signal."""
        k_series, d_series = self.indicators.calculate_stochastic(high, low, close)
        if k_series is None or d_series is None:
            return Signal.HOLD, {}
        k = float(k_series.iloc[-1])
        d = float(d_series.iloc[-1])
        result = {"k": round(k, 2), "d": round(d, 2)}
        if k < 20 and d < 20:
            return Signal.BUY, result
        if k > 80 and d > 80:
            return Signal.SELL, result
        return Signal.HOLD, result

    def analyze_williams_r(
        self,
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
    ) -> tuple[Signal, float]:
        """Generate Williams %R signal."""
        willr = self.indicators.calculate_williams_r(high, low, close)
        if willr is None:
            return Signal.HOLD, 0.0
        value = float(willr.iloc[-1])
        if value < -80:
            return Signal.BUY, value
        if value > -20:
            return Signal.SELL, value
        return Signal.HOLD, value

    def analyze_bollinger_bands(self, prices: pd.Series) -> tuple[Signal, dict]:
        """Generate Bollinger Band squeeze/break signal."""
        upper, middle, lower = self.indicators.calculate_bollinger_bands(prices)
        if upper is None:
            return Signal.HOLD, {}
        latest_price = float(prices.iloc[-1])
        result = {
            "price": latest_price,
            "upper": float(upper.iloc[-1]),
            "middle": float(middle.iloc[-1]),
            "lower": float(lower.iloc[-1]),
        }
        if latest_price <= float(lower.iloc[-1]):
            return Signal.BUY, result
        if latest_price >= float(upper.iloc[-1]):
            return Signal.SELL, result
        return Signal.HOLD, result

    def analyze_volume(self, volume: pd.Series, prices: pd.Series) -> tuple[Signal, dict]:
        """Generate a volume-trend confirmation signal.

        Rising volume with rising price confirms bullish momentum; falling price
        with rising volume confirms bearish pressure.
        """
        if len(volume) < 20:
            return Signal.HOLD, {}
        avg_volume = float(volume.rolling(20).mean().iloc[-1])
        latest_volume = float(volume.iloc[-1])
        price_change = float(prices.iloc[-1]) - float(prices.iloc[-2])
        volume_ratio = round(latest_volume / avg_volume if avg_volume > 0 else 1.0, 2)
        result = {"volume": latest_volume, "avg_volume_20d": round(avg_volume, 0), "volume_ratio": volume_ratio}
        if volume_ratio > 1.5 and price_change > 0:
            return Signal.BUY, result
        if volume_ratio > 1.5 and price_change < 0:
            return Signal.SELL, result
        return Signal.HOLD, result

    def calculate_position_size(
        self,
        account_value: float,
        latest_price: float,
        atr_value: float,
        risk_pct: float = 0.01,
    ) -> dict:
        """ATR-based position sizing with fixed fractional risk.

        Args:
            account_value: Total account equity in dollars.
            latest_price:  Current price of the instrument.
            atr_value:     14-period ATR value.
            risk_pct:      Fraction of account to risk per trade (default 1%).

        Returns:
            Dict with ``shares``, ``stop_loss``, and ``dollar_risk``.
        """
        if atr_value <= 0 or latest_price <= 0:
            return {"shares": 0, "stop_loss": 0.0, "dollar_risk": 0.0}
        dollar_risk = account_value * risk_pct
        stop_distance = atr_value * 2
        shares = int(dollar_risk / stop_distance)
        stop_loss = round(latest_price - stop_distance, 2)
        return {
            "shares": shares,
            "stop_loss": stop_loss,
            "dollar_risk": round(dollar_risk, 2),
        }

    def generate_technical_signal(self, ticker: str, period: str = "3mo") -> dict:
        """Download OHLCV data and generate a combined technical signal.

        Args:
            ticker: Stock ticker symbol.
            period: yfinance period string (e.g. ``"3mo"``).

        Returns:
            Dictionary with ``signal``, ``confidence``, ``latest_price``,
            ``price_change_percent``, and breakdowns per indicator.
        """
        logger.info("Generating technical signal for %s", ticker)
        try:
            data = yf.download(ticker, period=period, progress=False)
            if data.empty:
                logger.error("No data available for %s", ticker)
                return {"ticker": ticker, "signal": Signal.HOLD.value, "error": "No data"}

            prices = data["Close"]
            rsi_signal, rsi_value = self.analyze_rsi(prices)
            macd_signal, macd_data = self.analyze_macd(prices)
            ma_signal, ma_data = self.analyze_moving_averages(prices)
            bb_signal, bb_data = self.analyze_bollinger_bands(prices)

            buy_count = sum(1 for s in [rsi_signal, macd_signal, ma_signal, bb_signal] if s == Signal.BUY)
            sell_count = sum(1 for s in [rsi_signal, macd_signal, ma_signal, bb_signal] if s == Signal.SELL)

            if buy_count >= 3:
                overall = Signal.STRONG_BUY
            elif buy_count == 2:
                overall = Signal.BUY
            elif sell_count >= 3:
                overall = Signal.STRONG_SELL
            elif sell_count == 2:
                overall = Signal.SELL
            else:
                overall = Signal.HOLD

            latest_price = float(prices.iloc[-1])
            price_change = ((latest_price - float(prices.iloc[0])) / float(prices.iloc[0])) * 100

            result = {
                "ticker": ticker,
                "signal": overall.value,
                "confidence": round((buy_count + sell_count) / 4, 3),
                "latest_price": round(latest_price, 2),
                "price_change_percent": round(price_change, 2),
                "buy_signals": buy_count,
                "sell_signals": sell_count,
                "individual_signals": {
                    "rsi": rsi_signal.value,
                    "macd": macd_signal.value,
                    "moving_average": ma_signal.value,
                    "bollinger_bands": bb_signal.value,
                },
                "technical_data": {
                    "rsi": round(rsi_value, 2) if rsi_value else None,
                    "macd": macd_data,
                    "ma": ma_data,
                    "bb": bb_data,
                },
                "timestamp": datetime.now().isoformat(),
            }
            logger.info("Technical signal for %s: %s", ticker, overall.value)
            return result
        except Exception:
            logger.exception("Error generating technical signal for %s", ticker)
            return {"ticker": ticker, "signal": Signal.HOLD.value, "error": "Analysis failed"}


class SentimentSignalGenerator:
    """Derive a trading signal from aggregated sentiment scores."""

    def generate_sentiment_signal(self, sentiment_scores: list[dict]) -> Signal:
        """Convert a list of sentiment dicts to a Signal.

        Args:
            sentiment_scores: Each dict should have a ``combined_sentiment`` key
                with values ``"positive"``, ``"negative"``, or ``"neutral"``.

        Returns:
            A Signal enum value.
        """
        if not sentiment_scores:
            return Signal.HOLD

        total = len(sentiment_scores)
        positive_count = sum(1 for s in sentiment_scores if s.get("combined_sentiment") == "positive")
        negative_count = sum(1 for s in sentiment_scores if s.get("combined_sentiment") == "negative")

        positive_ratio = positive_count / total
        negative_ratio = negative_count / total

        if positive_ratio > 0.6:
            return Signal.STRONG_BUY
        if positive_ratio > 0.4:
            return Signal.BUY
        if negative_ratio > 0.6:
            return Signal.STRONG_SELL
        if negative_ratio > 0.4:
            return Signal.SELL
        return Signal.HOLD


class ComprehensiveSignalEngine:
    """Combine technical and sentiment signals into a final recommendation."""

    def __init__(self) -> None:
        self.technical_generator = TechnicalSignalGenerator()
        self.sentiment_generator = SentimentSignalGenerator()

    def generate_signal(
        self,
        ticker: str,
        sentiment_scores: Optional[list[dict]] = None,
        weights: Optional[dict[str, float]] = None,
    ) -> dict:
        """Generate a comprehensive trading signal.

        Args:
            ticker: Stock ticker symbol.
            sentiment_scores: Optional list of sentiment dicts from NLP analysis.
            weights: Dict with ``"technical"`` and ``"sentiment"`` keys (must sum to 1.0).

        Returns:
            Dictionary with ``final_signal``, ``combined_score``, ``technical``,
            ``sentiment``, ``weights``, and ``timestamp``.
        """
        logger.info("Generating comprehensive signal for %s", ticker)
        if weights is None:
            weights = {"technical": 0.7, "sentiment": 0.3}

        technical_result = self.technical_generator.generate_technical_signal(ticker)
        technical_signal = Signal[technical_result.get("signal", "HOLD")]
        technical_score = self._signal_to_score(technical_signal)

        sentiment_signal = Signal.HOLD
        sentiment_score = 0.0
        if sentiment_scores:
            sentiment_signal = self.sentiment_generator.generate_sentiment_signal(sentiment_scores)
            sentiment_score = self._signal_to_score(sentiment_signal)

        combined_score = technical_score * weights["technical"] + sentiment_score * weights["sentiment"]

        if combined_score > 0.8:
            final_signal = Signal.STRONG_BUY
        elif combined_score > 0.3:
            final_signal = Signal.BUY
        elif combined_score < -0.8:
            final_signal = Signal.STRONG_SELL
        elif combined_score < -0.3:
            final_signal = Signal.SELL
        else:
            final_signal = Signal.HOLD

        return {
            "ticker": ticker,
            "final_signal": final_signal.value,
            "combined_score": round(combined_score, 3),
            "technical": {
                "signal": technical_result.get("signal"),
                "confidence": round(technical_result.get("confidence", 0), 3),
                "latest_price": technical_result.get("latest_price"),
                "price_change_percent": technical_result.get("price_change_percent"),
            },
            "sentiment": {
                "signal": sentiment_signal.value,
                "articles_analyzed": len(sentiment_scores) if sentiment_scores else 0,
            },
            "weights": weights,
            "timestamp": datetime.now().isoformat(),
        }

    @staticmethod
    @lru_cache(maxsize=None)
    def _signal_to_score(signal: Signal) -> float:
        """Map a Signal enum to a numeric score in [-1, 1].

        Cached with lru_cache since the mapping is a pure function.
        """
        scores: dict[Signal, float] = {
            Signal.STRONG_BUY: 1.0,
            Signal.BUY: 0.5,
            Signal.HOLD: 0.0,
            Signal.SELL: -0.5,
            Signal.STRONG_SELL: -1.0,
        }
        return scores.get(signal, 0.0)
