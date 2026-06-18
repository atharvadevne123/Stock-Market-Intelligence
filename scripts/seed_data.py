"""Development seed script — populates a local SQLite database with sample data.

Usage::

    python scripts/seed_data.py
    python scripts/seed_data.py --db sqlite:///./dev.db
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Allow running from the repo root without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.database import DatabaseService
from database.models import Base, UserPreferences, WatchList

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

SAMPLE_TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

SAMPLE_ARTICLES = [
    ("AAPL", "Apple reports record iPhone sales", "Revenue beat estimates by 8% in Q1.", "Reuters"),
    ("MSFT", "Microsoft Azure growth accelerates", "Cloud revenue up 29% year-over-year.", "Bloomberg"),
    ("GOOGL", "Google unveils next-gen AI assistant", "Gemini Ultra to power new Pixel phones.", "TechCrunch"),
    ("AMZN", "Amazon expands same-day delivery", "New fulfilment centres open in 12 cities.", "WSJ"),
    ("TSLA", "Tesla cuts Model Y prices again", "Third price reduction in six months.", "CNBC"),
]

SAMPLE_SIGNALS = [
    ("AAPL", "BUY",        0.7,  0.4, 0.8, 0.75, 185.5,  1.5),
    ("MSFT", "STRONG_BUY", 0.9,  0.5, 0.9, 0.85, 420.0,  2.0),
    ("GOOGL","HOLD",       0.0,  0.1, 0.1, 0.5,  175.0,  0.5),
    ("AMZN", "SELL",      -0.6, -0.3,-0.5, 0.3,  190.0, -1.0),
    ("TSLA", "STRONG_SELL",-0.85,-0.7,-0.9, 0.25, 165.0, -2.0),
]


def seed(db_url: str) -> None:
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        log.info("Seeding articles…")
        for i, (ticker, title, content, source) in enumerate(SAMPLE_ARTICLES):
            url = f"https://example.com/seed-article-{i}"
            DatabaseService.save_article(session, ticker, title, content, source, url)

        log.info("Seeding signals…")
        for ticker, action, tech, sent, combo, conf, price, score in SAMPLE_SIGNALS:
            DatabaseService.save_signal(session, ticker, action, tech, sent, combo, conf, price, score)

        log.info("Seeding watchlists…")
        wl = WatchList(name="Tech Giants", tickers=", ".join(SAMPLE_TICKERS), description="Large-cap tech stocks")
        session.add(wl)

        log.info("Seeding user preferences…")
        prefs = [
            UserPreferences(key="theme", value="dark", description="UI theme"),
            UserPreferences(key="default_ticker", value="AAPL", description="Default analysis ticker"),
        ]
        for pref in prefs:
            session.add(pref)

        session.commit()
        log.info("Seed complete — %d articles, %d signals, 1 watchlist, %d prefs",
                 len(SAMPLE_ARTICLES), len(SAMPLE_SIGNALS), len(prefs))
    except Exception:
        session.rollback()
        log.exception("Seed failed")
        sys.exit(1)
    finally:
        session.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed development database")
    parser.add_argument("--db", default="sqlite:///./dev.db", help="SQLAlchemy database URL")
    args = parser.parse_args()
    seed(args.db)
