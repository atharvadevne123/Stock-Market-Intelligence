"""Simple vectorised backtester for evaluating signal strategies."""

from __future__ import annotations

import numpy as np
import pandas as pd


class SimpleBacktester:
    """Evaluate a buy/sell signal series against a price series.

    The strategy is fully invested (long-only): holds when signal is BUY,
    moves to cash otherwise.

    Example::

        bt = SimpleBacktester()
        result = bt.run(prices, signals)
        print(result["total_return"])
    """

    def __init__(self, initial_capital: float = 10_000.0, commission: float = 0.001) -> None:
        self.initial_capital = initial_capital
        self.commission = commission

    def run(self, prices: pd.Series, signals: pd.Series) -> dict:
        """Run the backtest.

        Args:
            prices:  Daily closing price series (same index length as *signals*).
            signals: Series of values where 1 = long, 0 = cash, -1 = short-cash.

        Returns:
            Dict with ``total_return``, ``annualised_return``, ``max_drawdown``,
            ``num_trades``, ``sharpe_ratio``, and ``equity_curve``.
        """
        if prices.empty or signals.empty:
            return {
                "total_return": 0.0,
                "annualised_return": 0.0,
                "max_drawdown": 0.0,
                "num_trades": 0,
                "sharpe_ratio": 0.0,
                "equity_curve": pd.Series(dtype=float),
            }

        signals = signals.reindex(prices.index).fillna(0)
        position = signals.shift(1).fillna(0)

        daily_returns = prices.pct_change().fillna(0)
        strategy_returns = position * daily_returns

        commission_costs = self.commission * position.diff().abs().fillna(0)
        net_returns = strategy_returns - commission_costs

        equity_curve = self.initial_capital * (1 + net_returns).cumprod()

        total_return = float(equity_curve.iloc[-1] / self.initial_capital - 1)
        n_days = len(prices)
        years = n_days / 252
        annualised_return = float((1 + total_return) ** (1 / years) - 1) if years > 0 else 0.0

        rolling_max = equity_curve.cummax()
        drawdown = (equity_curve - rolling_max) / rolling_max
        max_drawdown = float(-drawdown.min()) if not drawdown.empty else 0.0

        num_trades = int(position.diff().abs().sum() / 2)

        std = net_returns.std()
        sharpe = float(net_returns.mean() / std * np.sqrt(252)) if std > 0 else 0.0

        return {
            "total_return": round(total_return, 4),
            "annualised_return": round(annualised_return, 4),
            "max_drawdown": round(max_drawdown, 4),
            "num_trades": num_trades,
            "sharpe_ratio": round(sharpe, 3),
            "equity_curve": equity_curve,
        }
