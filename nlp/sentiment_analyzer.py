"""FinBERT Sentiment Analysis Module for Stock Market Intelligence.

Uses HuggingFace ProsusAI/finbert for financial sentiment scoring.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class SentimentScore:
    """Result of a single sentiment analysis inference."""

    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    POSITIVE = "positive"

    def __init__(
        self,
        text: str,
        sentiment: str,
        confidence: float,
        scores: dict[str, float],
    ) -> None:
        self.text = text
        self.sentiment = sentiment
        self.confidence = confidence
        self.scores = scores
        self.timestamp = datetime.now()

    def to_dict(self) -> dict:
        """Serialise to a plain dictionary."""
        return {
            "text": self.text,
            "sentiment": self.sentiment,
            "confidence": self.confidence,
            "scores": self.scores,
            "timestamp": self.timestamp.isoformat(),
        }

    def __repr__(self) -> str:
        return f"SentimentScore(sentiment={self.sentiment}, confidence={self.confidence:.2%})"


class FinBERTSentimentAnalyzer:
    """FinBERT-based sentiment analyser for financial news texts."""

    def __init__(
        self,
        model_name: str = "ProsusAI/finbert",
        device: int | None = None,
    ) -> None:
        """Initialise and load the FinBERT model.

        Args:
            model_name: HuggingFace model identifier.
            device: Device index (0 = CUDA, -1 = CPU). Auto-detected if None.
        """
        import torch
        from transformers import (
            AutoModelForSequenceClassification,
            AutoTokenizer,
            pipeline,
        )

        self.model_name = model_name

        if device is None:
            self.device = 0 if torch.cuda.is_available() else -1
        else:
            self.device = device

        device_name = "CUDA" if self.device == 0 else "CPU"
        logger.info("Loading FinBERT from %s on %s…", model_name, device_name)

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.pipeline = pipeline(
                "sentiment-analysis",
                model=self.model,
                tokenizer=self.tokenizer,
                device=self.device,
                truncation=True,
                max_length=512,
            )
            self.label2id: dict[str, int] = self.model.config.label2id
            self.id2label: dict[int, str] = {v: k for k, v in self.label2id.items()}
            logger.info("FinBERT loaded. Labels: %s", list(self.id2label.values()))
        except Exception:
            logger.exception("Failed to load FinBERT model %s", model_name)
            raise

    def analyze_sentiment(self, text: str) -> SentimentScore:
        """Analyse the sentiment of a single text snippet.

        Args:
            text: Raw text to classify.

        Returns:
            SentimentScore with label, confidence, and per-class scores.
        """
        import torch

        if not text or not text.strip():
            logger.warning("Empty text supplied; returning NEUTRAL")
            return SentimentScore(
                text=text,
                sentiment=SentimentScore.NEUTRAL,
                confidence=1.0,
                scores={SentimentScore.NEUTRAL: 1.0},
            )

        try:
            prediction = self.pipeline(text)[0]
            sentiment = prediction["label"].lower()
            confidence: float = prediction["score"]

            with torch.no_grad():
                inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(
                    self.model.device
                )
                logits = self.model(**inputs).logits
                probs = torch.softmax(logits, dim=-1)[0]

            scores = {self.id2label[i]: float(probs[i].item()) for i in range(len(self.id2label))}

            logger.debug("Sentiment: %s (%.2f%%)", sentiment, confidence * 100)
            return SentimentScore(
                text=text[:200] + "…" if len(text) > 200 else text,
                sentiment=sentiment,
                confidence=confidence,
                scores=scores,
            )
        except Exception:
            logger.exception("Error analysing sentiment; returning NEUTRAL")
            return SentimentScore(
                text=text,
                sentiment=SentimentScore.NEUTRAL,
                confidence=0.5,
                scores={SentimentScore.NEUTRAL: 0.5},
            )

    def analyze_batch(self, texts: list[str]) -> list[SentimentScore]:
        """Analyse sentiment of multiple texts.

        Args:
            texts: Sequence of strings to classify.

        Returns:
            List of SentimentScore objects in the same order as *texts*.
        """
        logger.info("Batch analysis: %d texts", len(texts))
        results = [self.analyze_sentiment(t) for t in texts]
        logger.info("Batch analysis complete")
        return results


class AggregatedSentiment:
    """Aggregate sentiment metrics across a collection of SentimentScore objects."""

    def __init__(self, scores: list[SentimentScore]) -> None:
        self.scores = scores
        self.count = len(scores)
        self._calculate_metrics()

    def _calculate_metrics(self) -> None:
        if self.count == 0:
            self.positive_ratio = 0.0
            self.negative_ratio = 0.0
            self.neutral_ratio = 0.0
            self.average_confidence = 0.0
            self.sentiment_trend = "NEUTRAL"
            return

        positive = sum(1 for s in self.scores if s.sentiment == SentimentScore.POSITIVE)
        negative = sum(1 for s in self.scores if s.sentiment == SentimentScore.NEGATIVE)

        self.positive_ratio = positive / self.count
        self.negative_ratio = negative / self.count
        self.neutral_ratio = 1.0 - self.positive_ratio - self.negative_ratio
        self.average_confidence = sum(s.confidence for s in self.scores) / self.count

        if self.positive_ratio > self.negative_ratio + 0.1:
            self.sentiment_trend = "BULLISH"
        elif self.negative_ratio > self.positive_ratio + 0.1:
            self.sentiment_trend = "BEARISH"
        else:
            self.sentiment_trend = "NEUTRAL"

    def to_dict(self) -> dict:
        """Serialise aggregated metrics to a plain dictionary."""
        return {
            "count": self.count,
            "positive_ratio": round(self.positive_ratio, 3),
            "negative_ratio": round(self.negative_ratio, 3),
            "neutral_ratio": round(self.neutral_ratio, 3),
            "average_confidence": round(self.average_confidence, 3),
            "sentiment_trend": self.sentiment_trend,
        }

    def __repr__(self) -> str:
        return (
            f"AggregatedSentiment(trend={self.sentiment_trend}, "
            f"positive={self.positive_ratio:.1%}, negative={self.negative_ratio:.1%})"
        )


class NewsArticleSentimentAnalyzer:
    """Combine title and body sentiment to score a full news article."""

    def __init__(self) -> None:
        self.analyzer = FinBERTSentimentAnalyzer()

    def analyze_article_title(self, title: str) -> SentimentScore:
        """Analyse headline sentiment."""
        return self.analyzer.analyze_sentiment(title)

    def analyze_article_content(self, content: str) -> SentimentScore:
        """Analyse body-text sentiment."""
        if not content or not content.strip():
            return self.analyzer.analyze_sentiment("")
        return self.analyzer.analyze_sentiment(content)

    def analyze_article(self, title: str, content: str) -> dict:
        """Analyse a complete article by weighting title and content scores.

        Args:
            title: Article headline.
            content: Article body text.

        Returns:
            Dictionary with title_sentiment, content_sentiment, combined_sentiment,
            combined_confidence, and all_scores.
        """
        title_sentiment = self.analyze_article_title(title)
        content_sentiment = self.analyze_article_content(content)

        title_is_neutral = title_sentiment.sentiment == "neutral"
        title_weight = 0.5 if title_is_neutral else 0.6
        content_weight = 1.0 - title_weight

        def _weighted(key: str) -> float:
            return (
                title_sentiment.scores.get(key, 0.0) * title_weight
                + content_sentiment.scores.get(key, 0.0) * content_weight
            )

        scores = {
            "positive": _weighted("positive"),
            "negative": _weighted("negative"),
            "neutral": _weighted("neutral"),
        }
        overall_sentiment = max(scores, key=scores.__getitem__)
        overall_confidence = max(scores.values())

        return {
            "title_sentiment": title_sentiment.to_dict(),
            "content_sentiment": content_sentiment.to_dict(),
            "combined_sentiment": overall_sentiment,
            "combined_confidence": round(overall_confidence, 3),
            "all_scores": {k: round(v, 3) for k, v in scores.items()},
        }
