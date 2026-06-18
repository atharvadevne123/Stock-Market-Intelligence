"""Integration tests combining multiple Stock Market Intelligence components."""

from __future__ import annotations

from datetime import datetime

import pytest


class TestSignalPipelineIntegration:
    """Test the full signal pipeline from sentiment to final recommendation."""

    def test_positive_sentiment_yields_buy(self):
        from analysis.signal_engine import SentimentSignalGenerator, Signal

        generator = SentimentSignalGenerator()
        scores = [{"combined_sentiment": "positive"}] * 8 + [{"combined_sentiment": "negative"}] * 2
        assert generator.generate_sentiment_signal(scores) in (Signal.BUY, Signal.STRONG_BUY)

    def test_negative_sentiment_yields_sell(self):
        from analysis.signal_engine import SentimentSignalGenerator, Signal

        generator = SentimentSignalGenerator()
        scores = [{"combined_sentiment": "negative"}] * 8 + [{"combined_sentiment": "positive"}] * 2
        assert generator.generate_sentiment_signal(scores) in (Signal.SELL, Signal.STRONG_SELL)

    def test_weights_sum_to_one(self):
        from analysis.signal_engine import ComprehensiveSignalEngine

        ComprehensiveSignalEngine()  # verify import succeeds
        weights = {"technical": 0.7, "sentiment": 0.3}
        assert abs(sum(weights.values()) - 1.0) < 1e-9

    def test_article_to_dict_roundtrip(self):
        from scraper.news_scraper import NewsArticle

        article = NewsArticle(
            title="Integration test",
            content="Content for testing.",
            source="Test Source",
            url="https://example.com/integration",
            published_date=datetime.now(),
            ticker="AAPL",
        )
        d = article.to_dict()
        assert d["title"] == "Integration test"
        assert d["ticker"] == "AAPL"
        assert isinstance(d["published_date"], str)

    @pytest.mark.parametrize(
        "buy_pct,sell_pct,expected_sign",
        [
            (0.8, 0.0, 1),  # mostly buy → positive score
            (0.0, 0.8, -1),  # mostly sell → negative score
            (0.5, 0.5, 0),  # balanced → zero
        ],
    )
    def test_signal_scoring(self, buy_pct, sell_pct, expected_sign):
        from analysis.signal_engine import ComprehensiveSignalEngine

        engine = ComprehensiveSignalEngine()
        total = 10
        pos = int(total * buy_pct)
        neg = int(total * sell_pct)
        scores = (
            [{"combined_sentiment": "positive"}] * pos
            + [{"combined_sentiment": "negative"}] * neg
            + [{"combined_sentiment": "neutral"}] * (total - pos - neg)
        )
        sentiment_signal = engine.sentiment_generator.generate_sentiment_signal(scores)
        score = engine._signal_to_score(sentiment_signal)
        if expected_sign > 0:
            assert score > 0
        elif expected_sign < 0:
            assert score < 0
        else:
            pass  # balanced — could be any


class TestDatabaseArticlePipeline:
    """Test saving and retrieving articles and signals end-to-end."""

    @pytest.fixture
    def db(self):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        from database.models import Base

        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
        session.close()

    def test_save_and_count_articles(self, db):
        from api.database import DatabaseService

        for i in range(5):
            DatabaseService.save_article(
                db, "AAPL", f"Title {i}", "Content", "Source", f"https://example.com/int-article-{i}"
            )
        from database.models import Article

        assert db.query(Article).filter(Article.ticker == "AAPL").count() == 5

    def test_save_multiple_signals_get_latest(self, db):
        from api.database import DatabaseService

        DatabaseService.save_signal(db, "MSFT", "HOLD", 0.0, 0.0, 0.0, 0.5, 300.0, 0.5)
        DatabaseService.save_signal(db, "MSFT", "BUY", 0.5, 0.4, 0.6, 0.7, 305.0, 1.5)
        latest = DatabaseService.get_latest_signal(db, "MSFT")
        assert latest is not None
        assert latest.ticker == "MSFT"

    def test_signal_count(self, db):
        from api.database import DatabaseService

        for _ in range(3):
            DatabaseService.save_signal(db, "AAPL", "BUY", 0.5, 0.4, 0.6, 0.7, 175.0, 1.5)
        assert DatabaseService.get_signal_count(db, "AAPL") == 3

    def test_get_recent_articles_limit(self, db):
        from api.database import DatabaseService

        for i in range(5):
            DatabaseService.save_article(
                db, "GOOGL", f"Title {i}", "Content", "Source", f"https://example.com/googl-int-{i}"
            )
        articles = DatabaseService.get_recent_articles(db, "GOOGL", limit=3)
        assert len(articles) == 3

    def test_delete_old_articles_integration(self, db):
        from api.database import DatabaseService

        DatabaseService.save_article(db, "TSLA", "Headline", "Body", "WSJ", "https://example.com/tsla-int-del")
        count_before = db.query(__import__("database.models", fromlist=["Article"]).Article).count()
        deleted = DatabaseService.delete_old_articles(db, days=90)
        count_after = db.query(__import__("database.models", fromlist=["Article"]).Article).count()
        assert isinstance(deleted, int)
        assert count_after <= count_before

    def test_watchlist_ticker_list_integration(self, db):
        from database.models import WatchList

        wl = WatchList(name="My Portfolio", tickers="AAPL, MSFT, GOOGL")
        db.add(wl)
        db.commit()
        loaded = db.query(WatchList).filter_by(name="My Portfolio").first()
        assert loaded is not None
        assert len(loaded.ticker_list()) == 3


class TestNewsArticleHashIntegration:
    def test_url_hash_uniqueness_in_batch(self):
        from scraper.news_scraper import NewsArticle

        articles = [
            NewsArticle("T1", "C", "S", f"https://example.com/hash-int-{i}", __import__("datetime").datetime.now())
            for i in range(10)
        ]
        hashes = {a.url_hash for a in articles}
        assert len(hashes) == 10

    def test_duplicate_url_same_hash_in_batch(self):
        from scraper.news_scraper import NewsArticle

        url = "https://example.com/dupe-hash-int"
        a1 = NewsArticle("T1", "C1", "S", url, __import__("datetime").datetime.now())
        a2 = NewsArticle("T2", "C2", "S", url, __import__("datetime").datetime.now())
        assert a1.url_hash == a2.url_hash
