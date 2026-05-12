"""Tests for api.database DatabaseService."""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def sqlite_engine():
    engine = create_engine("sqlite:///:memory:")
    from database.models import Base
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def db_session(sqlite_engine):
    Session = sessionmaker(bind=sqlite_engine)
    session = Session()
    yield session
    session.close()


class TestDatabaseService:
    def test_save_article_returns_article(self, db_session):
        from api.database import DatabaseService
        result = DatabaseService.save_article(
            db_session, "AAPL", "Test Title", "Test content", "Reuters",
            "https://example.com/unique-article-1"
        )
        assert result is not None
        assert result.ticker == "AAPL"

    def test_save_article_persists(self, db_session):
        from api.database import DatabaseService
        from database.models import Article
        DatabaseService.save_article(
            db_session, "MSFT", "MSFT Title", "Content", "Bloomberg",
            "https://example.com/unique-msft-1"
        )
        count = db_session.query(Article).filter(Article.ticker == "MSFT").count()
        assert count == 1

    def test_save_signal_returns_signal(self, db_session):
        from api.database import DatabaseService
        result = DatabaseService.save_signal(
            db_session, "AAPL", "BUY", 0.5, 0.4, 0.3, 0.7, 175.0, 2.5
        )
        assert result is not None
        assert result.signal_type == "BUY"

    def test_get_signal_history_empty(self, db_session):
        from api.database import DatabaseService
        result = DatabaseService.get_signal_history(db_session, "UNKNOWN")
        assert isinstance(result, list)
        assert len(result) == 0

    def test_get_latest_signal_none_when_empty(self, db_session):
        from api.database import DatabaseService
        result = DatabaseService.get_latest_signal(db_session, "UNKNOWN")
        assert result is None

    def test_save_and_retrieve_signal(self, db_session):
        from api.database import DatabaseService
        DatabaseService.save_signal(
            db_session, "AAPL", "HOLD", 0.0, 0.0, 0.0, 0.5, 180.0, 1.0
        )
        result = DatabaseService.get_latest_signal(db_session, "AAPL")
        assert result is not None
        assert result.ticker == "AAPL"

    def test_save_sentiment(self, db_session):
        from api.database import DatabaseService
        result = DatabaseService.save_sentiment(
            db_session, "AAPL", "positive", 0.9, 0.9, 0.05, 0.05
        )
        assert result is not None
        assert result.sentiment == "positive"
