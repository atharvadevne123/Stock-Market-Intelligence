"""
FinBERT Sentiment Analysis Module for Stock Market Intelligence
Uses HuggingFace FinBERT model for financial sentiment scoring
"""

import logging
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SentimentScore:
    """Data class for sentiment analysis result"""
    
    # Sentiment labels
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    POSITIVE = "positive"
    
    def __init__(self, text: str, sentiment: str, confidence: float, 
                 scores: Dict[str, float]):
        self.text = text
        self.sentiment = sentiment
        self.confidence = confidence
        self.scores = scores  # All class scores
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'text': self.text,
            'sentiment': self.sentiment,
            'confidence': self.confidence,
            'scores': self.scores,
            'timestamp': self.timestamp.isoformat()
        }
    
    def __repr__(self) -> str:
        return f"SentimentScore(sentiment={self.sentiment}, confidence={self.confidence:.2%})"


class FinBERTSentimentAnalyzer:
    """FinBERT-based sentiment analyzer for financial texts"""
    
    def __init__(self, model_name: str = "ProsusAI/finbert", device: str = None):
        """
        Initialize FinBERT analyzer
        
        Args:
            model_name: HuggingFace model name (default: ProsusAI/finbert)
            device: Device to use ('cuda' or 'cpu', auto-detected if None)
        """
        self.model_name = model_name
        
        # Auto-detect device
        if device is None:
            self.device = 0 if torch.cuda.is_available() else -1
            device_name = "CUDA (GPU)" if self.device == 0 else "CPU"
        else:
            self.device = device
            device_name = "CUDA (GPU)" if device == 0 else "CPU"
        
        logger.info(f"Loading FinBERT from {model_name} on {device_name}...")
        
        try:
            # Initialize tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            
            # Create pipeline for classification
            self.pipeline = pipeline(
                "sentiment-analysis",
                model=self.model,
                tokenizer=self.tokenizer,
                device=self.device,
                truncation=True,
                max_length=512
            )
            
            # Get label mappings
            self.label2id = self.model.config.label2id
            self.id2label = {v: k for k, v in self.label2id.items()}
            
            logger.info(f"FinBERT loaded successfully. Labels: {list(self.id2label.values())}")
            
        except Exception as e:
            logger.error(f"Error loading FinBERT: {e}")
            raise
    
    def analyze_sentiment(self, text: str) -> SentimentScore:
        """
        Analyze sentiment of a single text
        
        Args:
            text: Text to analyze
            
        Returns:
            SentimentScore object
        """
        if not text or len(text.strip()) == 0:
            logger.warning("Empty text provided for sentiment analysis")
            return SentimentScore(
                text=text,
                sentiment=SentimentScore.NEUTRAL,
                confidence=1.0,
                scores={SentimentScore.NEUTRAL: 1.0}
            )
        
        try:
            # Get prediction
            prediction = self.pipeline(text)[0]
            
            # Parse results
            sentiment = prediction['label'].lower()
            confidence = prediction['score']
            
            # Get all scores
            with torch.no_grad():
                inputs = self.tokenizer(
                    text,
                    return_tensors="pt",
                    truncation=True,
                    max_length=512
                ).to(self.model.device)
                
                logits = self.model(**inputs).logits
                probs = torch.softmax(logits, dim=-1)[0]
            
            scores = {
                self.id2label[i]: float(probs[i].item())
                for i in range(len(self.id2label))
            }
            
            result = SentimentScore(
                text=text[:200] + "..." if len(text) > 200 else text,
                sentiment=sentiment,
                confidence=confidence,
                scores=scores
            )
            
            logger.info(f"Analyzed text: {sentiment} ({confidence:.2%})")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            # Return neutral on error
            return SentimentScore(
                text=text,
                sentiment=SentimentScore.NEUTRAL,
                confidence=0.5,
                scores={SentimentScore.NEUTRAL: 0.5}
            )
    
    def analyze_batch(self, texts: List[str]) -> List[SentimentScore]:
        """
        Analyze sentiment of multiple texts
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            List of SentimentScore objects
        """
        logger.info(f"Analyzing batch of {len(texts)} texts...")
        results = []
        
        for i, text in enumerate(texts):
            result = self.analyze_sentiment(text)
            results.append(result)
            
            if (i + 1) % 10 == 0:
                logger.info(f"Processed {i + 1}/{len(texts)} texts")
        
        logger.info(f"Batch analysis complete")
        return results


class AggregatedSentiment:
    """Aggregated sentiment metrics for multiple texts"""
    
    def __init__(self, scores: List[SentimentScore]):
        self.scores = scores
        self.count = len(scores)
        self._calculate_metrics()
    
    def _calculate_metrics(self):
        """Calculate aggregated metrics"""
        if self.count == 0:
            self.positive_ratio = 0.0
            self.negative_ratio = 0.0
            self.neutral_ratio = 0.0
            self.average_confidence = 0.0
            self.sentiment_trend = "NEUTRAL"
            return
        
        # Count sentiments
        positive = sum(1 for s in self.scores if s.sentiment == SentimentScore.POSITIVE)
        negative = sum(1 for s in self.scores if s.sentiment == SentimentScore.NEGATIVE)
        neutral = sum(1 for s in self.scores if s.sentiment == SentimentScore.NEUTRAL)
        
        self.positive_ratio = positive / self.count
        self.negative_ratio = negative / self.count
        self.neutral_ratio = neutral / self.count
        
        # Average confidence
        self.average_confidence = sum(s.confidence for s in self.scores) / self.count
        
        # Determine overall trend
        if self.positive_ratio > self.negative_ratio + 0.1:
            self.sentiment_trend = "BULLISH"
        elif self.negative_ratio > self.positive_ratio + 0.1:
            self.sentiment_trend = "BEARISH"
        else:
            self.sentiment_trend = "NEUTRAL"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'count': self.count,
            'positive_ratio': round(self.positive_ratio, 3),
            'negative_ratio': round(self.negative_ratio, 3),
            'neutral_ratio': round(self.neutral_ratio, 3),
            'average_confidence': round(self.average_confidence, 3),
            'sentiment_trend': self.sentiment_trend
        }
    
    def __repr__(self) -> str:
        return (
            f"AggregatedSentiment(trend={self.sentiment_trend}, "
            f"positive={self.positive_ratio:.1%}, negative={self.negative_ratio:.1%})"
        )


class NewsArticleSentimentAnalyzer:
    """Analyze sentiment of news articles"""
    
    def __init__(self):
        self.analyzer = FinBERTSentimentAnalyzer()
    
    def analyze_article_title(self, title: str) -> SentimentScore:
        """Analyze sentiment of article title"""
        return self.analyzer.analyze_sentiment(title)
    
    def analyze_article_content(self, content: str) -> SentimentScore:
        """Analyze sentiment of article content"""
        if not content or len(content.strip()) == 0:
            return self.analyzer.analyze_sentiment("")
        
        # For long content, just analyze the content directly
        return self.analyzer.analyze_sentiment(content)
    
    def analyze_article(self, title: str, content: str) -> Dict:
        """Analyze complete article (title + content)"""
        title_sentiment = self.analyze_article_title(title)
        content_sentiment = self.analyze_article_content(content)
        
        # If title is neutral, weight content more heavily (50/50)
        # If title has strong sentiment, weight title more (60/40)
        title_is_neutral = title_sentiment.sentiment == 'neutral'
        
        if title_is_neutral:
            title_weight = 0.5
            content_weight = 0.5
        else:
            title_weight = 0.6
            content_weight = 0.4
        
        combined_positive = (
            title_sentiment.scores.get('positive', 0) * title_weight +
            content_sentiment.scores.get('positive', 0) * content_weight
        )
        combined_negative = (
            title_sentiment.scores.get('negative', 0) * title_weight +
            content_sentiment.scores.get('negative', 0) * content_weight
        )
        combined_neutral = (
            title_sentiment.scores.get('neutral', 0) * title_weight +
            content_sentiment.scores.get('neutral', 0) * content_weight
        )
        
        # Determine overall sentiment (pick the highest score)
        scores = {
            'positive': combined_positive,
            'negative': combined_negative,
            'neutral': combined_neutral
        }
        
        overall_sentiment = max(scores, key=scores.get)
        overall_confidence = max(scores.values())
        
        return {
            'title_sentiment': title_sentiment.to_dict(),
            'content_sentiment': content_sentiment.to_dict(),
            'combined_sentiment': overall_sentiment,
            'combined_confidence': round(overall_confidence, 3),
            'all_scores': {k: round(v, 3) for k, v in scores.items()}
        }


# Example usage and testing
if __name__ == "__main__":
    logger.info("Initializing FinBERT Sentiment Analyzer...")
    analyzer = FinBERTSentimentAnalyzer()
    
    # Test single text
    print("\n=== SINGLE TEXT ANALYSIS ===")
    test_texts = [
        "Apple stock surged on strong earnings beat and positive outlook",
        "The market declined significantly due to rising inflation concerns",
        "Trading was flat with mixed signals from corporate earnings"
    ]
    
    for text in test_texts:
        score = analyzer.analyze_sentiment(text)
        print(f"\nText: {text}")
        print(f"Sentiment: {score.sentiment} ({score.confidence:.2%})")
        print(f"Scores: {score.scores}")
    
    # Test batch analysis
    print("\n=== BATCH ANALYSIS ===")
    batch_scores = analyzer.analyze_batch(test_texts)
    aggregated = AggregatedSentiment(batch_scores)
    print(f"\nAggregated Results:")
    print(f"  Trend: {aggregated.sentiment_trend}")
    print(f"  Positive: {aggregated.positive_ratio:.1%}")
    print(f"  Negative: {aggregated.negative_ratio:.1%}")
    print(f"  Neutral: {aggregated.neutral_ratio:.1%}")
    
    # Test article analysis
    print("\n=== ARTICLE SENTIMENT ANALYSIS ===")
    article_analyzer = NewsArticleSentimentAnalyzer()
    
    article_result = article_analyzer.analyze_article(
        title="Tech Stocks Surge on AI Optimism",
        content="Major technology companies reported strong earnings driven by AI adoption. Investors showed renewed interest in the sector."
    )
    print(f"Article Sentiment Analysis:")
    print(f"  Combined Sentiment: {article_result['combined_sentiment'].upper()}")
    print(f"  Confidence: {article_result['combined_confidence']:.2%}")
    print(f"  Scores: {article_result['all_scores']}")
    
    print("\n✅ FinBERT sentiment analyzer working!")