"""Portfolio risk metrics for Stock Market Intelligence.

Provides Value-at-Risk (VaR), Sharpe ratio, and correlation analysis
using historical price data from yfinance.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class PortfolioRiskCalculator:
    """Calculate portfolio-level risk metrics from historical returns."""

    def __init__(self, risk_free_rate: float = 0.05) -> None:
        """Initialise the calculator.

        Args:
            risk_free_rate: Annual risk-free rate for Sharpe ratio (default 5%).
        """
        self.risk_free_rate = risk_free_rate

    def historical_var(
        self,
        returns: pd.Series,
        confidence: float = 0.95,
    ) -> float:
        """Compute historical Value-at-Risk at the given confidence level.

        Args:
            returns: Daily return series (e.g. ``prices.pct_change().dropna()``).
            confidence: Confidence level (default 0.95 → 95% VaR).

        Returns:
            VaR as a positive float (loss expressed as fraction of portfolio).
        """
        if returns.empty:
            return 0.0
        return float(-np.percentile(returns.dropna(), (1 - confidence) * 100))

    def sharpe_ratio(
        self,
        returns: pd.Series,
        trading_days: int = 252,
    ) -> float:
        """Compute the annualised Sharpe ratio.

        Args:
            returns: Daily return series.
            trading_days: Number of trading days per year (default 252).

        Returns:
            Annualised Sharpe ratio, or 0.0 if standard deviation is zero.
        """
        daily_rf = (1 + self.risk_free_rate) ** (1 / trading_days) - 1
        excess = returns.dropna() - daily_rf
        std = excess.std()
        if std == 0:
            return 0.0
        return float(excess.mean() / std * np.sqrt(trading_days))

    def max_drawdown(self, prices: pd.Series) -> float:
        """Compute the maximum drawdown from peak to trough.

        Args:
            prices: Price series (not returns).

        Returns:
            Maximum drawdown as a positive fraction (e.g. 0.25 = 25% drawdown).
        """
        if prices.empty:
            return 0.0
        rolling_max = prices.cummax()
        drawdown = (prices - rolling_max) / rolling_max
        return float(-drawdown.min())

    def portfolio_correlation(self, returns_df: pd.DataFrame) -> pd.DataFrame:
        """Compute the pairwise return correlation matrix.

        Args:
            returns_df: DataFrame where each column is a ticker's daily returns.

        Returns:
            Correlation matrix as a DataFrame.
        """
        return returns_df.corr()

    def portfolio_volatility(
        self,
        returns_df: pd.DataFrame,
        weights: Optional[list[float]] = None,
        trading_days: int = 252,
    ) -> float:
        """Compute annualised portfolio volatility (standard deviation of returns).

        Args:
            returns_df: DataFrame where each column is a ticker's daily returns.
            weights: Portfolio weights (equal-weight if None).
            trading_days: Trading days per year for annualisation.

        Returns:
            Annualised portfolio volatility as a fraction.
        """
        n = len(returns_df.columns)
        if weights is None:
            weights = [1.0 / n] * n
        w = np.array(weights)
        cov = returns_df.cov() * trading_days
        variance = float(w @ cov.values @ w)
        return float(np.sqrt(variance))

    def summary(self, prices: pd.Series, ticker: str = "") -> dict:
        """Return a summary dict of risk metrics for a single ticker.

        Args:
            prices: Price series.
            ticker: Optional label for the output dict.

        Returns:
            Dict with ``ticker``, ``var_95``, ``sharpe_ratio``, ``max_drawdown``,
            ``annualised_vol``, and ``timestamp``.
        """
        returns = prices.pct_change().dropna()
        return {
            "ticker": ticker,
            "var_95": round(self.historical_var(returns, 0.95), 4),
            "sharpe_ratio": round(self.sharpe_ratio(returns), 3),
            "max_drawdown": round(self.max_drawdown(prices), 4),
            "annualised_vol": round(returns.std() * np.sqrt(252), 4),
            "timestamp": datetime.now().isoformat(),
        }
