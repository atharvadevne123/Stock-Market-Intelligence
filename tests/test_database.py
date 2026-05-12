"""Tests for api.database DatabaseService."""
from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def engine():
    eng = create_engine("sqlite:///:memory:")
    from database.models import Base
    Base.metadata.create_all(eng)
    return eng


@pytest.fixture
def db(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


class TestSaveArticle:
    def test_returns_article(self, db):
        from api.database import DatabaseService
        result = DatabaseService.save_article(
            db, "AAPL", "Test", "Content", "Reuters", "https://example.com/test-1"
        )
        assert result is not None
        assert result.ticker == "AAPL"

    def test_persists_to_db(self, db):
        from api.database import DatabaseService
        from database.models import Article
        DatabaseService.save_article(db, "MSFT", "T", "C", "B", "https://example.com/msft-1")
        assert db.query(Article).filter(Article.ticker == "MSFT").count() == 1

    def test_duplicate_url_returns_none(self, db):
        from api.database import DatabaseService
        url = "https://example.com/unique-dup"
        DatabaseService.save_article(db, "AAPL", "T1", "C1", "S1", url)
        result = DatabaseService.save_article(db, "AAPL", "T2", "C2", "S2", url)
        assert result is None

    @pytest.mark.parametrize("ticker", ["AAPL", "MSFT", "GOOGL"])
    def test_various_tickers(self, db, ticker):
        from api.database import DatabaseService
        result = DatabaseService.save_article(
            db, ticker, "Title", "Content", "Source",
            f"https://example.com/{ticker.lower()}-unique-123"
        )
        assert result.ticker == ticker


class TestSaveSignal:
    def test_returns_signal(self, db):
        from api.database import DatabaseService
        result = DatabaseService.save_signal(db, "AAPL", "BUY", 0.5, 0.4, 0.3, 0.7, 175.0, 2.5)
        assert result is not None
        assert result.signal_type == "BUY"

    @pytest.mark.parametrize("signal_type", ["BUY", "SELL", "HOLD", "STRONG_BUY", "STRONG_SELL"])
    def test_all_signal_types(self, db, signal_type):
        from api.database import DatabaseService
        result = DatabaseService.save_signal(db, "TEST", signal_type, 0.0, 0.0, 0.0, 0.5, 100.0, 0.0)
        assert result.signal_type == signal_type


class TestSignalHistory:
    def test_empty_history(self, db):
        from api.database import DatabaseService
        assert DatabaseService.get_signal_history(db, "UNKNOWN") == []

    def test_history_ordered_newest_first(self, db):
        from api.database import DatabaseService
        DatabaseService.save_signal(db, "AAPL", "HOLD", 0.0, 0.0, 0.0, 0.5, 170.0, 0.0)
        DatabaseService.save_signal(db, "AAPL", "BUY", 0.5, 0.4, 0.6, 0.7, 175.0, 1.5)
        history = DatabaseService.get_signal_history(db, "AAPL")
        assert len(history) == 2

    def test_get_latest_signal(self, db):
        from api.database import DatabaseService
        DatabaseService.save_signal(db, "MSFT", "SELL", -0.5, -0.4, -0.6, 0.7, 290.0, -2.0)
        latest = DatabaseService.get_latest_signal(db, "MSFT")
        assert latest is not None
        assert latest.ticker == "MSFT"


class TestSaveSentiment:
    def test_returns_sentiment(self, db):
        from api.database import DatabaseService
        result = DatabaseService.save_sentiment(db, "AAPL", "positive", 0.9, 0.9, 0.05, 0.05)
        assert result is not None
        assert result.sentiment == "positive"

    @pytest.mark.parametrize("sentiment", ["positive", "negative", "neutral"])
    def test_all_sentiments(self, db, sentiment):
        from api.database import DatabaseService
        result = DatabaseService.save_sentiment(db, "TEST", sentiment, 0.8, 0.5, 0.3, 0.2)
        assert result.sentiment == sentiment
