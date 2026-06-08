"""Main orchestrator combining news, sentiment, and signal components."""

from __future__ import annotations

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    from analysis.signal_engine import ComprehensiveSignalEngine
except Exception:  # pragma: no cover
    ComprehensiveSignalEngine = None  # type: ignore[assignment,misc]

try:
    from scraper.news_scraper import NewsAggregator
except Exception:  # pragma: no cover
    NewsAggregator = None  # type: ignore[assignment,misc]

try:
    from nlp.sentiment_analyzer import NewsArticleSentimentAnalyzer
except Exception:  # pragma: no cover
    NewsArticleSentimentAnalyzer = None  # type: ignore[assignment,misc]


class StockMarketIntelligence:
    """Top-level orchestrator that wires together the full analysis pipeline."""

    def __init__(self) -> None:
        """Initialise all pipeline components."""
        logger.info("Initialising Stock Market Intelligence System…")
        self.news_aggregator = NewsAggregator()
        self.sentiment_analyzer = NewsArticleSentimentAnalyzer()
        self.signal_engine = ComprehensiveSignalEngine()
        logger.info("All components initialised successfully")

    def analyze_ticker(self, ticker: str, hours: int = 24) -> dict:
        """Run the full analysis pipeline for a single ticker.

        Args:
            ticker: Stock ticker symbol (e.g. ``"AAPL"``).
            hours: How many hours of historical news to include.

        Returns:
            Dictionary with ``ticker``, ``timestamp``, ``news``,
            ``sentiment``, ``signal``, and ``analysis_steps``.
        """
        logger.info("Starting comprehensive analysis for %s", ticker)
        result: dict = {
            "ticker": ticker,
            "timestamp": datetime.now().isoformat(),
            "analysis_steps": [],
        }

        try:
            logger.info("Step 1: Fetching news for %s", ticker)
            articles = self.news_aggregator.get_ticker_news(ticker, hours=hours)
            result["news"] = {
                "articles_found": len(articles),
                "articles": [a.to_dict() for a in articles[:5]],
            }
            result["analysis_steps"].append("News fetching complete")

            logger.info("Step 2: Analysing sentiment from %d articles", len(articles))
            sentiment_results: list[dict] = []
            for article in articles[:10]:
                try:
                    sentiment = self.sentiment_analyzer.analyze_article(
                        title=article.title,
                        content=article.content,
                    )
                    sentiment_results.append(sentiment)
                except Exception:
                    logger.warning("Sentiment failed for article: %s", article.title[:60])

            result["sentiment"] = {
                "articles_analyzed": len(sentiment_results),
                "results": sentiment_results[:3],
            }
            result["analysis_steps"].append("Sentiment analysis complete")

            logger.info("Step 3: Generating trading signal")
            signal = self.signal_engine.generate_signal(ticker, sentiment_scores=sentiment_results)
            result["signal"] = signal
            result["analysis_steps"].append("Signal generation complete")
            logger.info("Analysis complete for %s: %s", ticker, signal["final_signal"])

        except Exception:
            logger.exception("Error during analysis for %s", ticker)
            result["error"] = "Analysis failed — see server logs"

        return result

    def analyze_portfolio(self, tickers: list[str], hours: int = 24) -> dict:
        """Analyse multiple tickers and produce a portfolio summary.

        Args:
            tickers: List of ticker symbols.
            hours: News lookback window in hours.

        Returns:
            Dictionary with per-ticker analyses and an aggregate summary.
        """
        logger.info("Analysing portfolio of %d tickers", len(tickers))
        results: dict = {
            "portfolio": tickers,
            "timestamp": datetime.now().isoformat(),
            "analyses": [],
            "summary": {},
        }
        for i, ticker in enumerate(tickers, 1):
            logger.info("Analysing %s (%d/%d)…", ticker, i, len(tickers))
            analysis = self.analyze_ticker(ticker, hours=hours)
            results["analyses"].append(analysis)

        results["summary"] = self._generate_portfolio_summary(results["analyses"])
        logger.info("Portfolio analysis complete")
        return results

    def _generate_portfolio_summary(self, analyses: list[dict]) -> dict:
        """Aggregate signal distribution across a portfolio."""
        signal_counts: dict[str, int] = {"STRONG_BUY": 0, "BUY": 0, "HOLD": 0, "SELL": 0, "STRONG_SELL": 0}
        for analysis in analyses:
            sig = analysis.get("signal", {}).get("final_signal")
            if sig in signal_counts:
                signal_counts[sig] += 1

        return {
            "total_analyzed": len(analyses),
            "signal_distribution": signal_counts,
            "recommendation": self._get_portfolio_recommendation(signal_counts),
        }

    @staticmethod
    def _get_portfolio_recommendation(signal_counts: dict[str, int]) -> str:
        """Return a high-level portfolio stance based on signal distribution."""
        buy_signals = signal_counts["STRONG_BUY"] + signal_counts["BUY"]
        sell_signals = signal_counts["STRONG_SELL"] + signal_counts["SELL"]
        if buy_signals > sell_signals + 1:
            return "BULLISH"
        if sell_signals > buy_signals + 1:
            return "BEARISH"
        return "NEUTRAL"

    def get_market_overview(self, hours: int = 24) -> dict:
        """Summarise overall market sentiment from recent news.

        Args:
            hours: How many hours of news to aggregate.

        Returns:
            Dictionary with ``market_sentiment``, ``articles_analyzed``,
            ``sentiment_distribution``, and ``timestamp``.
        """
        logger.info("Generating market overview…")
        try:
            market_news = self.news_aggregator.get_market_news(hours=hours)
            sentiment_results: list[dict] = []
            for article in market_news[:20]:
                try:
                    sentiment = self.sentiment_analyzer.analyze_article(title=article.title, content=article.content)
                    sentiment_results.append(sentiment)
                except Exception:
                    pass

            if not sentiment_results:
                return {
                    "market_sentiment": "NEUTRAL",
                    "articles_analyzed": 0,
                    "timestamp": datetime.now().isoformat(),
                }

            positive = sum(1 for s in sentiment_results if s.get("combined_sentiment") == "positive")
            negative = sum(1 for s in sentiment_results if s.get("combined_sentiment") == "negative")
            total = len(sentiment_results)

            if positive / total > 0.5:
                market_sentiment = "BULLISH"
            elif negative / total > 0.5:
                market_sentiment = "BEARISH"
            else:
                market_sentiment = "NEUTRAL"

            return {
                "market_sentiment": market_sentiment,
                "articles_analyzed": total,
                "sentiment_distribution": {
                    "positive": positive,
                    "negative": negative,
                    "neutral": total - positive - negative,
                },
                "timestamp": datetime.now().isoformat(),
            }
        except Exception:
            logger.exception("Error generating market overview")
            return {
                "market_sentiment": "NEUTRAL",
                "articles_analyzed": 0,
                "error": "Overview failed",
                "timestamp": datetime.now().isoformat(),
            }
