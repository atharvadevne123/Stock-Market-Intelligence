"""Signal generation and technical analysis package.

This package provides the ComprehensiveSignalEngine that combines
technical indicators (RSI, MACD, Bollinger Bands, Moving Averages)
with sentiment analysis to generate BUY/SELL/HOLD trading signals.
"""

from __future__ import annotations

from .signal_engine import (
    ComprehensiveSignalEngine,
    SentimentSignalGenerator,
    Signal,
    TechnicalIndicator,
    TechnicalSignalGenerator,
)

__version__ = "1.0.0"
__all__ = [
    "ComprehensiveSignalEngine",
    "Signal",
    "SentimentSignalGenerator",
    "TechnicalIndicator",
    "TechnicalSignalGenerator",
]
