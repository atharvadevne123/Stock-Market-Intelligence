"""Natural language processing and sentiment analysis package.

Provides FinBERT-based financial sentiment scoring via the
NewsArticleSentimentAnalyzer class, which handles title/body
weighting and aggregation across multiple articles.
"""
from __future__ import annotations

from .sentiment_analyzer import (
    AggregatedSentiment,
    FinBERTSentimentAnalyzer,
    NewsArticleSentimentAnalyzer,
    SentimentScore,
)

__version__ = "1.0.0"
__all__ = [
    "AggregatedSentiment",
    "FinBERTSentimentAnalyzer",
    "NewsArticleSentimentAnalyzer",
    "SentimentScore",
]
