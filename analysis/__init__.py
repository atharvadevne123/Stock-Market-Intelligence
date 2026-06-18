"""Signal generation, technical analysis, and portfolio risk package.

This package provides the ComprehensiveSignalEngine that combines
technical indicators (RSI, MACD, Bollinger Bands, Moving Averages)
with sentiment analysis to generate BUY/SELL/HOLD trading signals,
and PortfolioRiskCalculator for VaR, Sharpe ratio, and drawdown analysis.
"""

from __future__ import annotations

from .portfolio_risk import PortfolioRiskCalculator
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
    "PortfolioRiskCalculator",
    "Signal",
    "SentimentSignalGenerator",
    "TechnicalIndicator",
    "TechnicalSignalGenerator",
]
