"""Human-readable formatting helpers for financial values."""

from __future__ import annotations


def format_currency(value: float, symbol: str = "$", decimals: int = 2) -> str:
    """Format a numeric value as a currency string.

    >>> format_currency(1234.5)
    '$1,234.50'
    >>> format_currency(-99.9, symbol="£")
    '-£99.90'
    """
    sign = "-" if value < 0 else ""
    formatted = f"{abs(value):,.{decimals}f}"
    return f"{sign}{symbol}{formatted}"


def format_percentage(value: float, decimals: int = 2, multiply: bool = False) -> str:
    """Format a fractional or percentage value as a percentage string.

    Args:
        value: The numeric value.
        decimals: Number of decimal places.
        multiply: If True, multiply value by 100 first (e.g. 0.05 → "5.00%").

    >>> format_percentage(0.0523, multiply=True)
    '5.23%'
    >>> format_percentage(12.5)
    '12.50%'
    """
    pct = value * 100 if multiply else value
    return f"{pct:.{decimals}f}%"


def format_signal_label(signal: str) -> str:
    """Convert a raw signal string to a display-friendly label.

    >>> format_signal_label("STRONG_BUY")
    'Strong Buy'
    >>> format_signal_label("hold")
    'Hold'
    """
    return signal.replace("_", " ").title()
