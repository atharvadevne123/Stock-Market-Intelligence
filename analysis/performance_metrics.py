"""Extended performance metrics: CAGR, Sortino ratio, Calmar ratio."""

from __future__ import annotations

import numpy as np
import pandas as pd


class PerformanceMetrics:
    """Additional risk-adjusted performance metrics beyond Sharpe ratio."""

    def __init__(self, risk_free_rate: float = 0.05) -> None:
        self.risk_free_rate = risk_free_rate

    def cagr(self, prices: pd.Series) -> float:
        """Compute Compound Annual Growth Rate.

        Args:
            prices: Price series with at least two data points.

        Returns:
            CAGR as a fraction (e.g. 0.12 = 12% per year).
        """
        if len(prices) < 2:
            return 0.0
        years = len(prices) / 252
        if years <= 0:
            return 0.0
        start = float(prices.iloc[0])
        end = float(prices.iloc[-1])
        if start <= 0:
            return 0.0
        return float((end / start) ** (1 / years) - 1)

    def sortino_ratio(self, returns: pd.Series, trading_days: int = 252) -> float:
        """Compute the annualised Sortino ratio (penalises only downside volatility).

        Args:
            returns: Daily return series.
            trading_days: Trading days per year for annualisation.

        Returns:
            Annualised Sortino ratio, or 0.0 if downside deviation is zero.
        """
        daily_rf = (1 + self.risk_free_rate) ** (1 / trading_days) - 1
        excess = returns.dropna() - daily_rf
        downside = excess[excess < 0]
        if downside.empty:
            return 0.0
        downside_std = float(downside.std())
        if downside_std == 0:
            return 0.0
        return float(excess.mean() / downside_std * np.sqrt(trading_days))

    def calmar_ratio(self, prices: pd.Series) -> float:
        """Compute the Calmar ratio (CAGR / max drawdown).

        Args:
            prices: Price series.

        Returns:
            Calmar ratio, or 0.0 if max drawdown is zero.
        """
        annual_return = self.cagr(prices)
        rolling_max = prices.cummax()
        drawdown = (prices - rolling_max) / rolling_max
        max_dd = float(-drawdown.min()) if not prices.empty else 0.0
        if max_dd == 0:
            return 0.0
        return float(annual_return / max_dd)

    def summary(self, prices: pd.Series, ticker: str = "") -> dict:
        """Return a dict of extended metrics for *ticker*."""
        returns = prices.pct_change().dropna()
        return {
            "ticker": ticker,
            "cagr": round(self.cagr(prices), 4),
            "sortino_ratio": round(self.sortino_ratio(returns), 3),
            "calmar_ratio": round(self.calmar_ratio(prices), 3),
        }
