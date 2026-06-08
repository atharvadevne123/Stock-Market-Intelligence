"""Database service layer and FastAPI dependency for Stock Market Intelligence."""

from __future__ import annotations

import logging
from collections.abc import Generator
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session and ensures cleanup."""
    from database.models import SessionLocal

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


class DatabaseService:
    """Static service methods for persisting and querying stock intelligence data."""

    @staticmethod
    def save_article(db: Session, ticker: str, title: str, content: str, source: str, url: str):
        """Persist a news article. Returns None if URL already exists."""
        try:
            from database.models import Article

            article = Article(
                ticker=ticker,
                title=title,
                content=content,
                source=source,
                url=url,
                published_date=_utcnow(),
            )
            db.add(article)
            db.commit()
            db.refresh(article)
            return article
        except Exception:
            db.rollback()
            logger.exception("Error saving article for ticker %s", ticker)
            return None

    @staticmethod
    def save_signal(
        db: Session,
        ticker: str,
        signal_type: str,
        combined_score: float,
        technical_score: float,
        sentiment_score: float,
        confidence: float,
        latest_price: float,
        price_change_percent: float,
    ):
        """Persist a trading signal."""
        try:
            from database.models import Signal

            signal = Signal(
                ticker=ticker,
                signal_type=signal_type,
                combined_score=combined_score,
                technical_score=technical_score,
                sentiment_score=sentiment_score,
                confidence=confidence,
                latest_price=latest_price,
                price_change_percent=price_change_percent,
            )
            db.add(signal)
            db.commit()
            db.refresh(signal)
            return signal
        except Exception:
            db.rollback()
            logger.exception("Error saving signal for ticker %s", ticker)
            return None

    @staticmethod
    def save_sentiment(
        db: Session,
        ticker: str,
        sentiment: str,
        confidence: float,
        positive_score: float,
        negative_score: float,
        neutral_score: float,
    ):
        """Persist a sentiment result."""
        try:
            from database.models import Sentiment

            sentiment_obj = Sentiment(
                ticker=ticker,
                sentiment=sentiment,
                confidence=confidence,
                positive_score=positive_score,
                negative_score=negative_score,
                neutral_score=neutral_score,
            )
            db.add(sentiment_obj)
            db.commit()
            db.refresh(sentiment_obj)
            return sentiment_obj
        except Exception:
            db.rollback()
            logger.exception("Error saving sentiment for ticker %s", ticker)
            return None

    @staticmethod
    def get_signal_history(db: Session, ticker: str, days: int = 30) -> list:
        """Return recent signals for a ticker ordered newest first."""
        try:
            from database.models import Signal

            cutoff = _utcnow() - timedelta(days=days)
            return (
                db.query(Signal)
                .filter(Signal.ticker == ticker, Signal.created_at >= cutoff)
                .order_by(Signal.created_at.desc())
                .all()
            )
        except Exception:
            logger.exception("Error getting signal history for ticker %s", ticker)
            return []

    @staticmethod
    def get_latest_signal(db: Session, ticker: str):
        """Return the most recent signal for a ticker, or None."""
        try:
            from database.models import Signal

            return db.query(Signal).filter(Signal.ticker == ticker).order_by(Signal.created_at.desc()).first()
        except Exception:
            logger.exception("Error getting latest signal for ticker %s", ticker)
            return None

    @staticmethod
    def get_signal_count(db: Session, ticker: str) -> int:
        """Return the total number of signals stored for a ticker."""
        try:
            from database.models import Signal

            return db.query(Signal).filter(Signal.ticker == ticker).count()
        except Exception:
            logger.exception("Error counting signals for ticker %s", ticker)
            return 0

    @staticmethod
    def get_recent_articles(db: Session, ticker: str, limit: int = 10) -> list:
        """Return the most recently stored articles for a ticker."""
        try:
            from database.models import Article

            return (
                db.query(Article)
                .filter(Article.ticker == ticker)
                .order_by(Article.created_at.desc())
                .limit(limit)
                .all()
            )
        except Exception:
            logger.exception("Error getting articles for ticker %s", ticker)
            return []
