"""Signal generation, technical analysis, portfolio risk, and backtesting package.

This package provides the ComprehensiveSignalEngine that combines
technical indicators (RSI, MACD, Bollinger Bands, Moving Averages)
with sentiment analysis to generate BUY/SELL/HOLD trading signals,
PortfolioRiskCalculator for VaR, Sharpe ratio, and drawdown analysis,
PerformanceMetrics for CAGR/Sortino/Calmar, and SimpleBacktester.
"""

from __future__ import annotations

from .backtester import SimpleBacktester
from .performance_metrics import PerformanceMetrics
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
    "PerformanceMetrics",
    "PortfolioRiskCalculator",
    "Signal",
    "SentimentSignalGenerator",
    "SimpleBacktester",
    "TechnicalIndicator",
    "TechnicalSignalGenerator",
]
