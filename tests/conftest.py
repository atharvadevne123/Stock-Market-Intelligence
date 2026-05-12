"""Pytest fixtures for Stock Market Intelligence tests."""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
import numpy as np


@pytest.fixture
def sample_ticker():
    """Return a sample stock ticker."""
    return "AAPL"


@pytest.fixture
def sample_sentiment_scores():
    """Return sample sentiment score dictionaries."""
    return [
        {"combined_sentiment": "positive", "combined_confidence": 0.85},
        {"combined_sentiment": "positive", "combined_confidence": 0.78},
        {"combined_sentiment": "neutral", "combined_confidence": 0.60},
    ]


@pytest.fixture
def sample_article_data():
    """Return sample article data."""
    return {
        "title": "Apple Reports Record Quarterly Revenue",
        "content": "Apple Inc. beat earnings expectations with strong iPhone sales.",
        "source": "Reuters",
        "url": "https://example.com/apple-earnings",
    }


@pytest.fixture
def mock_price_series():
    """Return a mock price Series with enough data for indicators."""
    dates = pd.date_range("2023-01-01", periods=250, freq="B")
    rng = np.random.default_rng(42)
    prices = pd.Series(
        rng.uniform(150, 200, 250),
        index=dates,
        name="Close",
    )
    return prices


@pytest.fixture
def mock_ohlcv_df(mock_price_series):
    """Return a mock OHLCV DataFrame."""
    prices = mock_price_series
    rng = np.random.default_rng(42)
    df = pd.DataFrame(
        {
            "Close": prices.values,
            "High": prices.values * 1.02,
            "Low": prices.values * 0.98,
            "Open": prices.values * 0.99,
            "Volume": rng.integers(1_000_000, 5_000_000, len(prices)),
        },
        index=prices.index,
    )
    return df


@pytest.fixture
def mock_yf_download(mock_ohlcv_df):
    """Patch yfinance.download to return mock OHLCV data."""
    with patch("yfinance.download", return_value=mock_ohlcv_df) as mock:
        yield mock


@pytest.fixture
def mock_news_articles():
    """Return a list of mock NewsArticle-like dicts."""
    from datetime import datetime

    return [
        {
            "title": "Apple beats Q4 earnings",
            "content": "Strong iPhone demand drives revenue growth.",
            "source": "Reuters",
            "url": "https://example.com/1",
            "published_date": datetime.now().isoformat(),
            "ticker": "AAPL",
        },
        {
            "title": "Market volatility rises",
            "content": "Investors cautious ahead of Fed decision.",
            "source": "Bloomberg",
            "url": "https://example.com/2",
            "published_date": datetime.now().isoformat(),
            "ticker": None,
        },
    ]
