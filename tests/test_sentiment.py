"""Tests for nlp.sentiment_analyzer module."""

from __future__ import annotations

from unittest.mock import MagicMock, patch


class TestSentimentScore:
    @patch("transformers.AutoTokenizer.from_pretrained")
    @patch("transformers.AutoModelForSequenceClassification.from_pretrained")
    @patch("transformers.pipeline")
    def test_to_dict_keys(self, mock_pipeline, mock_model, mock_tokenizer):
        from nlp.sentiment_analyzer import SentimentScore

        score = SentimentScore(
            text="Apple stock rose 5%",
            sentiment="positive",
            confidence=0.92,
            scores={"positive": 0.92, "negative": 0.04, "neutral": 0.04},
        )
        d = score.to_dict()
        assert "text" in d
        assert "sentiment" in d
        assert "confidence" in d
        assert "scores" in d
        assert "timestamp" in d

    @patch("transformers.AutoTokenizer.from_pretrained")
    @patch("transformers.AutoModelForSequenceClassification.from_pretrained")
    @patch("transformers.pipeline")
    def test_sentiment_values(self, mock_pipeline, mock_model, mock_tokenizer):
        from nlp.sentiment_analyzer import SentimentScore

        for sentiment in ("positive", "negative", "neutral"):
            score = SentimentScore(
                text="Test",
                sentiment=sentiment,
                confidence=0.8,
                scores={sentiment: 0.8},
            )
            assert score.sentiment == sentiment

    @patch("transformers.AutoTokenizer.from_pretrained")
    @patch("transformers.AutoModelForSequenceClassification.from_pretrained")
    @patch("transformers.pipeline")
    def test_repr(self, mock_pipeline, mock_model, mock_tokenizer):
        from nlp.sentiment_analyzer import SentimentScore

        score = SentimentScore("x", "positive", 0.95, {})
        repr_str = repr(score)
        assert "SentimentScore" in repr_str
        assert "positive" in repr_str


class TestNewsArticleSentimentAnalyzer:
    @patch("transformers.AutoTokenizer.from_pretrained")
    @patch("transformers.AutoModelForSequenceClassification.from_pretrained")
    @patch("transformers.pipeline")
    def test_analyze_article_returns_dict(self, mock_pipeline, mock_model, mock_tokenizer):
        mock_pipe = MagicMock()
        mock_pipe.return_value = [{"label": "positive", "score": 0.9}]
        mock_pipeline.return_value = mock_pipe

        from nlp.sentiment_analyzer import NewsArticleSentimentAnalyzer, SentimentScore

        analyzer = NewsArticleSentimentAnalyzer()
        analyzer.analyzer = MagicMock()
        analyzer.analyzer.analyze_sentiment.return_value = SentimentScore(
            text="test",
            sentiment="positive",
            confidence=0.9,
            scores={"positive": 0.9, "negative": 0.05, "neutral": 0.05},
        )
        result = analyzer.analyze_article("Great earnings", "Strong results reported.")
        assert "combined_sentiment" in result
        assert "all_scores" in result

    @patch("transformers.AutoTokenizer.from_pretrained")
    @patch("transformers.AutoModelForSequenceClassification.from_pretrained")
    @patch("transformers.pipeline")
    def test_analyze_article_combined_sentiment_valid(self, mock_pipeline, mock_model, mock_tokenizer):
        mock_pipe = MagicMock()
        mock_pipe.return_value = [{"label": "positive", "score": 0.9}]
        mock_pipeline.return_value = mock_pipe

        from nlp.sentiment_analyzer import NewsArticleSentimentAnalyzer, SentimentScore

        analyzer = NewsArticleSentimentAnalyzer()
        analyzer.analyzer = MagicMock()
        analyzer.analyzer.analyze_sentiment.return_value = SentimentScore(
            text="test",
            sentiment="positive",
            confidence=0.9,
            scores={"positive": 0.9, "negative": 0.05, "neutral": 0.05},
        )
        result = analyzer.analyze_article("test title", "test content")
        assert result["combined_sentiment"] in ("positive", "negative", "neutral")
