"""Debug helper to quickly test the sentiment analyser from the CLI."""

from __future__ import annotations

import argparse
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    """Entry point for the debug sentiment CLI."""
    parser = argparse.ArgumentParser(description="Debug FinBERT sentiment analyser")
    parser.add_argument("--title", default="Apple Beats Earnings", help="Article headline")
    parser.add_argument("--content", default="Strong Q4 results", help="Article body")
    args = parser.parse_args(argv)

    logger.info("Loading NewsArticleSentimentAnalyzer...")
    try:
        from nlp.sentiment_analyzer import NewsArticleSentimentAnalyzer

        analyzer = NewsArticleSentimentAnalyzer()
    except Exception:
        logger.exception("Failed to load analyser")
        return 1

    title_result = analyzer.analyze_article_title(args.title)
    logger.info("Title scores: %s", title_result.scores)

    content_result = analyzer.analyze_article_content(args.content)
    logger.info("Content scores: %s", content_result.scores)

    result = analyzer.analyze_article(args.title, args.content)
    logger.info("Combined sentiment: %s", result["combined_sentiment"])
    logger.info("All scores: %s", result["all_scores"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
