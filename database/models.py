"""
SQLAlchemy ORM Models for Stock Market Intelligence
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/stock_intelligence")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Article(Base):
    """News article model"""
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), index=True)
    title = Column(String(500))
    content = Column(Text)
    source = Column(String(100))
    url = Column(String(500), unique=True)
    published_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)


class Signal(Base):
    """Trading signals"""
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), index=True)
    signal_type = Column(String(20))
    combined_score = Column(Float)
    technical_score = Column(Float)
    sentiment_score = Column(Float)
    confidence = Column(Float)
    latest_price = Column(Float)
    price_change_percent = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class Sentiment(Base):
    """Sentiment analysis results"""
    __tablename__ = "sentiments"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), index=True)
    sentiment = Column(String(20))
    confidence = Column(Float)
    positive_score = Column(Float)
    negative_score = Column(Float)
    neutral_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class Portfolio(Base):
    """User portfolios"""
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)
    tickers = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)


class BacktestResult(Base):
    """Backtesting results"""
    __tablename__ = "backtest_results"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), index=True)
    strategy = Column(String(100))
    total_return = Column(Float)
    win_rate = Column(Float)
    sharpe_ratio = Column(Float)
    trades_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized!")


if __name__ == "__main__":
    init_db()
