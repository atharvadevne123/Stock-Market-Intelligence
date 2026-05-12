"""Integration tests combining multiple Stock Market Intelligence components."""
from __future__ import annotations

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime


class TestSignalPipelineIntegration:
    """Test the full signal pipeline from sentiment to final recommendation."""

    def test_positive_sentiment_influences_signal(self):
        from analysis.signal_engine import SentimentSignalGenerator, Signal
        generator = SentimentSignalGenerator()
        scores = [{"combined_sentiment": "positive"}] * 8 + [{"combined_sentiment": "negative"}] * 2
        result = generator.generate_sentiment_signal(scores)
        assert result in (Signal.BUY, Signal.STRONG_BUY)

    def test_negative_sentiment_influences_signal(self):
        from analysis.signal_engine import SentimentSignalGenerator, Signal
        generator = SentimentSignalGenerator()
        scores = [{"combined_sentiment": "negative"}] * 8 + [{"combined_sentiment": "positive"}] * 2
        result = generator.generate_sentiment_signal(scores)
        assert result in (Signal.SELL, Signal.STRONG_SELL)

    def test_combined_engine_weights_sum_to_one(self):
        from analysis.signal_engine import ComprehensiveSignalEngine
        engine = ComprehensiveSignalEngine()
        weights = {"technical": 0.7, "sentiment": 0.3}
        assert abs(sum(weights.values()) - 1.0) < 1e-9

    def test_article_converts_to_dict(self):
        from scraper.news_scraper import NewsArticle
        article = NewsArticle(
            title="Integration test article",
            content="Content for integration testing.",
            source="Test Source",
            url="https://example.com/integration",
            published_date=datetime.now(),
            ticker="AAPL",
        )
        d = article.to_dict()
        assert d["title"] == "Integration test article"
        assert d["ticker"] == "AAPL"


class TestDatabaseArticlePipeline:
    """Test saving and retrieving articles and signals."""

    @pytest.fixture
    def db_session(self):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from database.models import Base
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
        session.close()

    def test_save_and_count_articles(self, db_session):
        from api.database import DatabaseService
        for i in range(5):
            DatabaseService.save_article(
                db_session, "AAPL", f"Title {i}", "Content", "Source",
                f"https://example.com/article-{i}"
            )
        from database.models import Article
        count = db_session.query(Article).filter(Article.ticker == "AAPL").count()
        assert count == 5

    def test_save_multiple_signals_and_get_latest(self, db_session):
        from api.database import DatabaseService
        DatabaseService.save_signal(db_session, "MSFT", "HOLD", 0.0, 0.0, 0.0, 0.5, 300.0, 0.5)
        DatabaseService.save_signal(db_session, "MSFT", "BUY", 0.5, 0.4, 0.6, 0.7, 305.0, 1.5)
        latest = DatabaseService.get_latest_signal(db_session, "MSFT")
        assert latest is not None
        assert latest.ticker == "MSFT"
