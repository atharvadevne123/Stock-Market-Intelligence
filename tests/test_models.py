"""Tests for database.models SQLAlchemy models."""

from __future__ import annotations

from datetime import datetime

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from database.models import (
    Article,
    BacktestResult,
    Base,
    Portfolio,
    Sentiment,
    Signal,
)


@pytest.fixture
def engine():
    eng = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(eng)
    return eng


@pytest.fixture
def session(engine):
    Session = sessionmaker(bind=engine)
    s = Session()
    yield s
    s.close()


class TestArticleModel:
    def test_create_article(self, session):
        article = Article(
            ticker="AAPL",
            title="Strong Earnings",
            content="Revenue record.",
            source="Reuters",
            url="https://example.com/aapl-v2-1",
            published_date=datetime.utcnow(),
        )
        session.add(article)
        session.commit()
        assert article.id is not None

    def test_article_repr(self, session):
        article = Article(
            ticker="AAPL",
            title="Test",
            content="x",
            source="y",
            url="https://example.com/aapl-repr-1",
            published_date=datetime.utcnow(),
        )
        session.add(article)
        session.commit()
        assert "AAPL" in repr(article)
        assert "Article" in repr(article)

    def test_article_ticker_indexed(self, engine):
        inspector = inspect(engine)
        indexes = inspector.get_indexes("articles")
        indexed_columns = [idx["column_names"] for idx in indexes]
        assert any("ticker" in cols for cols in indexed_columns)

    def test_article_created_at_auto(self, session):
        article = Article(
            ticker="MSFT",
            title="Test",
            content="x",
            source="y",
            url="https://example.com/msft-v2-1",
            published_date=datetime.utcnow(),
        )
        session.add(article)
        session.commit()
        assert article.created_at is not None


class TestSignalModel:
    def test_create_signal(self, session):
        sig = Signal(
            ticker="AAPL",
            signal_type="BUY",
            combined_score=0.6,
            technical_score=0.5,
            sentiment_score=0.7,
            confidence=0.8,
            latest_price=175.0,
            price_change_percent=2.5,
        )
        session.add(sig)
        session.commit()
        assert sig.id is not None

    def test_signal_repr(self, session):
        sig = Signal(
            ticker="AAPL",
            signal_type="SELL",
            combined_score=-0.5,
            technical_score=-0.4,
            sentiment_score=-0.6,
            confidence=0.7,
            latest_price=170.0,
            price_change_percent=-2.0,
        )
        session.add(sig)
        session.commit()
        assert "SELL" in repr(sig)

    @pytest.mark.parametrize("signal_type", ["BUY", "SELL", "HOLD", "STRONG_BUY", "STRONG_SELL"])
    def test_all_signal_types(self, session, signal_type):
        sig = Signal(
            ticker="TEST",
            signal_type=signal_type,
            combined_score=0.0,
            technical_score=0.0,
            sentiment_score=0.0,
            confidence=0.5,
            latest_price=100.0,
            price_change_percent=0.0,
        )
        session.add(sig)
        session.commit()
        assert sig.signal_type == signal_type


class TestSentimentModel:
    def test_create_sentiment(self, session):
        s = Sentiment(
            ticker="GOOGL",
            sentiment="positive",
            confidence=0.87,
            positive_score=0.87,
            negative_score=0.08,
            neutral_score=0.05,
        )
        session.add(s)
        session.commit()
        assert s.id is not None

    def test_sentiment_repr(self, session):
        s = Sentiment(
            ticker="TSLA",
            sentiment="negative",
            confidence=0.75,
            positive_score=0.1,
            negative_score=0.75,
            neutral_score=0.15,
        )
        session.add(s)
        session.commit()
        assert "TSLA" in repr(s) and "negative" in repr(s)


class TestPortfolioModel:
    def test_create_portfolio(self, session):
        p = Portfolio(name="Tech Portfolio", tickers="AAPL,MSFT,GOOGL")
        session.add(p)
        session.commit()
        assert p.id is not None

    def test_portfolio_repr(self, session):
        p = Portfolio(name="My Portfolio", tickers="AAPL")
        session.add(p)
        session.commit()
        assert "My Portfolio" in repr(p)


class TestBacktestResultModel:
    def test_create(self, session):
        br = BacktestResult(
            ticker="AAPL",
            strategy="RSI_MACD",
            total_return=15.3,
            win_rate=0.62,
            sharpe_ratio=1.4,
            trades_count=48,
        )
        session.add(br)
        session.commit()
        assert br.id is not None

    def test_backtest_repr(self, session):
        br = BacktestResult(
            ticker="MSFT",
            strategy="MACD_BB",
            total_return=8.5,
            win_rate=0.55,
            sharpe_ratio=1.1,
            trades_count=30,
        )
        session.add(br)
        session.commit()
        assert "MSFT" in repr(br)


class TestWatchListModel:
    def test_create_watchlist(self, session):
        from database.models import WatchList

        wl = WatchList(name="Tech Giants", tickers="AAPL,MSFT,GOOGL")
        session.add(wl)
        session.commit()
        assert wl.id is not None

    def test_ticker_list_method(self, session):
        from database.models import WatchList

        wl = WatchList(name="EV", tickers="TSLA, RIVN, LCID")
        assert wl.ticker_list() == ["TSLA", "RIVN", "LCID"]

    def test_repr(self, session):
        from database.models import WatchList

        wl = WatchList(name="My List", tickers="AAPL")
        session.add(wl)
        session.commit()
        assert "My List" in repr(wl)

    def test_description_optional(self, session):
        from database.models import WatchList

        wl = WatchList(name="No Desc", tickers="AAPL")
        session.add(wl)
        session.commit()
        assert wl.description is None

    @pytest.mark.parametrize("name,tickers", [
        ("Momentum", "AAPL,MSFT"),
        ("Dividend", "JNJ,PG,KO"),
        ("Growth", "AMZN,GOOGL,META"),
    ])
    def test_various_watchlists(self, session, name: str, tickers: str):
        from database.models import WatchList

        wl = WatchList(name=name, tickers=tickers)
        session.add(wl)
        session.commit()
        assert wl.name == name
        assert len(wl.ticker_list()) > 0


class TestUserPreferencesModel:
    def test_create_preference(self, session):
        from database.models import UserPreferences

        pref = UserPreferences(key="default_hours", value="24")
        session.add(pref)
        session.commit()
        assert pref.id is not None

    def test_unique_key_constraint(self, session):
        from sqlalchemy.exc import IntegrityError

        from database.models import UserPreferences

        session.add(UserPreferences(key="theme", value="dark"))
        session.commit()
        session.add(UserPreferences(key="theme", value="light"))
        with pytest.raises(IntegrityError):
            session.commit()

    def test_repr(self, session):
        from database.models import UserPreferences

        pref = UserPreferences(key="notify", value="true")
        session.add(pref)
        session.commit()
        assert "notify" in repr(pref)

    @pytest.mark.parametrize("key,value", [
        ("refresh_interval", "60"),
        ("max_tickers", "10"),
        ("signal_threshold", "0.7"),
    ])
    def test_various_preferences(self, session, key: str, value: str):
        from database.models import UserPreferences

        pref = UserPreferences(key=key, value=value)
        session.add(pref)
        session.commit()
        assert pref.key == key
        assert pref.value == value


class TestInitDb:
    def test_init_db_creates_tables(self):
        eng = create_engine("sqlite:///:memory:")
        from database import models

        models.engine = eng
        models.Base.metadata.create_all(eng)
        inspector = inspect(eng)
        tables = inspector.get_table_names()
        assert "articles" in tables
        assert "signals" in tables
        assert "sentiments" in tables

    def test_init_db_creates_watchlist_table(self):
        eng = create_engine("sqlite:///:memory:")
        from database import models

        models.Base.metadata.create_all(eng)
        tables = inspect(eng).get_table_names()
        assert "watchlists" in tables

    def test_init_db_creates_user_preferences_table(self):
        eng = create_engine("sqlite:///:memory:")
        from database import models

        models.Base.metadata.create_all(eng)
        tables = inspect(eng).get_table_names()
        assert "user_preferences" in tables
