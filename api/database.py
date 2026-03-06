"""
Database integration for FastAPI
"""

from sqlalchemy.orm import Session
from datetime import datetime

class DatabaseService:
    @staticmethod
    def save_article(db: Session, ticker: str, title: str, content: str, source: str, url: str):
        """Save article to database"""
        try:
            from database.models import Article
            article = Article(
                ticker=ticker,
                title=title,
                content=content,
                source=source,
                url=url,
                published_date=datetime.utcnow()
            )
            db.add(article)
            db.commit()
            return article
        except Exception as e:
            db.rollback()
            print(f"Error saving article: {e}")
            return None

    @staticmethod
    def save_signal(db: Session, ticker: str, signal_type: str, combined_score: float,
                    technical_score: float, sentiment_score: float, confidence: float,
                    latest_price: float, price_change_percent: float):
        """Save signal to database"""
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
                price_change_percent=price_change_percent
            )
            db.add(signal)
            db.commit()
            return signal
        except Exception as e:
            db.rollback()
            print(f"Error saving signal: {e}")
            return None

    @staticmethod
    def save_sentiment(db: Session, ticker: str, sentiment: str, confidence: float,
                      positive_score: float, negative_score: float, neutral_score: float):
        """Save sentiment to database"""
        try:
            from database.models import Sentiment
            sentiment_obj = Sentiment(
                ticker=ticker,
                sentiment=sentiment,
                confidence=confidence,
                positive_score=positive_score,
                negative_score=negative_score,
                neutral_score=neutral_score
            )
            db.add(sentiment_obj)
            db.commit()
            return sentiment_obj
        except Exception as e:
            db.rollback()
            print(f"Error saving sentiment: {e}")
            return None

    @staticmethod
    def get_signal_history(db: Session, ticker: str, days: int = 30):
        """Get signal history for a ticker"""
        try:
            from database.models import Signal
            from datetime import timedelta
            cutoff = datetime.utcnow() - timedelta(days=days)
            return db.query(Signal).filter(
                Signal.ticker == ticker,
                Signal.created_at >= cutoff
            ).order_by(Signal.created_at.desc()).all()
        except Exception as e:
            print(f"Error getting signal history: {e}")
            return []

    @staticmethod
    def get_latest_signal(db: Session, ticker: str):
        """Get latest signal for a ticker"""
        try:
            from database.models import Signal
            return db.query(Signal).filter(
                Signal.ticker == ticker
            ).order_by(Signal.created_at.desc()).first()
        except Exception as e:
            print(f"Error getting latest signal: {e}")
            return None
