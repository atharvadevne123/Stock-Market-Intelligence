"""
Signal Engine for Stock Market Intelligence
Combines sentiment analysis, technical indicators, and market data to generate BUY/SELL/HOLD signals
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import pandas as pd
import yfinance as yf
try:
    import pandas_ta as ta
except ImportError:
    import pandas_ta_classic as ta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Signal(Enum):
    """Trading signals"""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    STRONG_BUY = "STRONG_BUY"
    STRONG_SELL = "STRONG_SELL"


class TechnicalIndicator:
    """Calculate technical indicators"""
    
    @staticmethod
    def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        rsi = ta.rsi(prices, length=period)
        return rsi
    
    @staticmethod
    def calculate_macd(prices: pd.Series) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Calculate MACD (Moving Average Convergence Divergence)"""
        macd_result = ta.macd(prices)
        if macd_result is not None and len(macd_result.columns) >= 3:
            return macd_result.iloc[:, 0], macd_result.iloc[:, 1], macd_result.iloc[:, 2]
        return None, None, None
    
    @staticmethod
    def calculate_bollinger_bands(prices: pd.Series, period: int = 20) -> Tuple:
        """Calculate Bollinger Bands"""
        bb = ta.bbands(prices, length=period)
        if bb is not None and len(bb.columns) >= 3:
            return bb.iloc[:, 0], bb.iloc[:, 1], bb.iloc[:, 2]  # Upper, Mid, Lower
        return None, None, None
    
    @staticmethod
    def calculate_moving_averages(prices: pd.Series) -> Tuple[pd.Series, pd.Series]:
        """Calculate 50-day and 200-day moving averages"""
        ma50 = ta.sma(prices, length=50)
        ma200 = ta.sma(prices, length=200)
        return ma50, ma200
    
    @staticmethod
    def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, 
                     period: int = 14) -> pd.Series:
        """Calculate Average True Range"""
        atr = ta.atr(high, low, close, length=period)
        return atr


class TechnicalSignalGenerator:
    """Generate signals based on technical indicators"""
    
    def __init__(self):
        self.indicators = TechnicalIndicator()
    
    def analyze_rsi(self, prices: pd.Series) -> Tuple[Signal, float]:
        """Generate signal based on RSI"""
        rsi = self.indicators.calculate_rsi(prices)
        latest_rsi = rsi.iloc[-1]
        
        if latest_rsi > 70:
            return Signal.SELL, latest_rsi
        elif latest_rsi < 30:
            return Signal.BUY, latest_rsi
        else:
            return Signal.HOLD, latest_rsi
    
    def analyze_macd(self, prices: pd.Series) -> Tuple[Signal, Dict]:
        """Generate signal based on MACD"""
        macd_line, signal_line, histogram = self.indicators.calculate_macd(prices)
        
        if macd_line is None:
            return Signal.HOLD, {}
        
        latest_macd = macd_line.iloc[-1]
        latest_signal = signal_line.iloc[-1]
        latest_hist = histogram.iloc[-1]
        prev_hist = histogram.iloc[-2]
        
        result = {
            'macd': latest_macd,
            'signal': latest_signal,
            'histogram': latest_hist
        }
        
        # MACD above signal line and histogram increasing
        if latest_macd > latest_signal and latest_hist > prev_hist:
            return Signal.BUY, result
        # MACD below signal line and histogram decreasing
        elif latest_macd < latest_signal and latest_hist < prev_hist:
            return Signal.SELL, result
        else:
            return Signal.HOLD, result
    
    def analyze_moving_averages(self, prices: pd.Series) -> Tuple[Signal, Dict]:
        """Generate signal based on moving average crossover"""
        ma50, ma200 = self.indicators.calculate_moving_averages(prices)
        latest_price = prices.iloc[-1]
        latest_ma50 = ma50.iloc[-1]
        latest_ma200 = ma200.iloc[-1]
        
        result = {
            'price': latest_price,
            'ma50': latest_ma50,
            'ma200': latest_ma200
        }
        
        # Golden cross (50 > 200) and price above both
        if latest_ma50 > latest_ma200 and latest_price > latest_ma50:
            return Signal.BUY, result
        # Death cross (50 < 200) and price below both
        elif latest_ma50 < latest_ma200 and latest_price < latest_ma50:
            return Signal.SELL, result
        else:
            return Signal.HOLD, result
    
    def analyze_bollinger_bands(self, prices: pd.Series) -> Tuple[Signal, Dict]:
        """Generate signal based on Bollinger Bands"""
        upper, middle, lower = self.indicators.calculate_bollinger_bands(prices)
        
        if upper is None:
            return Signal.HOLD, {}
        
        latest_price = prices.iloc[-1]
        latest_upper = upper.iloc[-1]
        latest_middle = middle.iloc[-1]
        latest_lower = lower.iloc[-1]
        
        result = {
            'price': latest_price,
            'upper': latest_upper,
            'middle': latest_middle,
            'lower': latest_lower
        }
        
        # Price touching lower band (potential buy)
        if latest_price <= latest_lower:
            return Signal.BUY, result
        # Price touching upper band (potential sell)
        elif latest_price >= latest_upper:
            return Signal.SELL, result
        else:
            return Signal.HOLD, result
    
    def generate_technical_signal(self, ticker: str, period: str = "3mo") -> Dict:
        """Generate combined technical signal for a ticker"""
        logger.info(f"Generating technical signal for {ticker}...")
        
        try:
            # Download data
            data = yf.download(ticker, period=period, progress=False)
            
            if data.empty:
                logger.error(f"No data available for {ticker}")
                return {
                    'ticker': ticker,
                    'signal': Signal.HOLD.value,
                    'error': 'No data available'
                }
            
            prices = data['Close']
            high = data['High']
            low = data['Low']
            
            # Get individual signals
            rsi_signal, rsi_value = self.analyze_rsi(prices)
            macd_signal, macd_data = self.analyze_macd(prices)
            ma_signal, ma_data = self.analyze_moving_averages(prices)
            bb_signal, bb_data = self.analyze_bollinger_bands(prices)
            
            # Count signals
            buy_count = sum(1 for s in [rsi_signal, macd_signal, ma_signal, bb_signal] 
                          if s == Signal.BUY)
            sell_count = sum(1 for s in [rsi_signal, macd_signal, ma_signal, bb_signal] 
                           if s == Signal.SELL)
            
            # Determine overall signal
            if buy_count >= 3:
                overall_signal = Signal.STRONG_BUY
            elif buy_count == 2:
                overall_signal = Signal.BUY
            elif sell_count >= 3:
                overall_signal = Signal.STRONG_SELL
            elif sell_count == 2:
                overall_signal = Signal.SELL
            else:
                overall_signal = Signal.HOLD
            
            # Get latest price and change
            latest_price = prices.iloc[-1]
            price_change = ((latest_price - prices.iloc[0]) / prices.iloc[0]) * 100
            
            result = {
                'ticker': ticker,
                'signal': overall_signal.value,
                'confidence': (buy_count + sell_count) / 4,  # 0-1 scale
                'latest_price': round(latest_price, 2),
                'price_change_percent': round(price_change, 2),
                'buy_signals': buy_count,
                'sell_signals': sell_count,
                'individual_signals': {
                    'rsi': rsi_signal.value,
                    'macd': macd_signal.value,
                    'moving_average': ma_signal.value,
                    'bollinger_bands': bb_signal.value
                },
                'technical_data': {
                    'rsi': round(rsi_value, 2),
                    'macd': macd_data,
                    'ma': ma_data,
                    'bb': bb_data
                },
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Technical signal for {ticker}: {overall_signal.value}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating technical signal for {ticker}: {e}")
            return {
                'ticker': ticker,
                'signal': Signal.HOLD.value,
                'error': str(e)
            }


class SentimentSignalGenerator:
    """Generate signals based on sentiment analysis"""
    
    def generate_sentiment_signal(self, sentiment_scores: List[Dict]) -> Signal:
        """
        Generate signal from aggregated sentiment scores
        
        Args:
            sentiment_scores: List of sentiment analysis results
            
        Returns:
            Signal based on sentiment
        """
        if not sentiment_scores:
            return Signal.HOLD
        
        # Count sentiments
        positive_count = sum(1 for s in sentiment_scores 
                           if s.get('combined_sentiment') == 'positive')
        negative_count = sum(1 for s in sentiment_scores 
                           if s.get('combined_sentiment') == 'negative')
        total = len(sentiment_scores)
        
        positive_ratio = positive_count / total
        negative_ratio = negative_count / total
        
        if positive_ratio > 0.6:
            return Signal.STRONG_BUY
        elif positive_ratio > 0.4:
            return Signal.BUY
        elif negative_ratio > 0.6:
            return Signal.STRONG_SELL
        elif negative_ratio > 0.4:
            return Signal.SELL
        else:
            return Signal.HOLD


class ComprehensiveSignalEngine:
    """Combines all signals for final trading recommendation"""
    
    def __init__(self):
        self.technical_generator = TechnicalSignalGenerator()
        self.sentiment_generator = SentimentSignalGenerator()
    
    def generate_signal(self, 
                       ticker: str,
                       sentiment_scores: Optional[List[Dict]] = None,
                       weights: Optional[Dict] = None) -> Dict:
        """
        Generate comprehensive trading signal
        
        Args:
            ticker: Stock ticker symbol
            sentiment_scores: List of sentiment analysis results
            weights: Weights for technical (0-1) and sentiment (0-1)
            
        Returns:
            Comprehensive signal recommendation
        """
        logger.info(f"Generating comprehensive signal for {ticker}...")
        
        # Default weights
        if weights is None:
            weights = {'technical': 0.7, 'sentiment': 0.3}
        
        # Get technical signal
        technical_result = self.technical_generator.generate_technical_signal(ticker)
        technical_signal = Signal[technical_result.get('signal', 'HOLD')]
        technical_score = self._signal_to_score(technical_signal)
        
        # Get sentiment signal
        sentiment_signal = Signal.HOLD
        sentiment_score = 0.0
        
        if sentiment_scores:
            sentiment_signal = self.sentiment_generator.generate_sentiment_signal(
                sentiment_scores
            )
            sentiment_score = self._signal_to_score(sentiment_signal)
        
        # Combine signals
        combined_score = (
            technical_score * weights['technical'] +
            sentiment_score * weights['sentiment']
        )
        
        # Determine final signal
        if combined_score > 0.5:
            final_signal = Signal.STRONG_BUY if combined_score > 0.8 else Signal.BUY
        elif combined_score < -0.5:
            final_signal = Signal.STRONG_SELL if combined_score < -0.8 else Signal.SELL
        else:
            final_signal = Signal.HOLD
        
        result = {
            'ticker': ticker,
            'final_signal': final_signal.value,
            'combined_score': round(combined_score, 3),
            'technical': {
                'signal': technical_result.get('signal'),
                'confidence': round(technical_result.get('confidence', 0), 3),
                'latest_price': technical_result.get('latest_price'),
                'price_change_percent': technical_result.get('price_change_percent')
            },
            'sentiment': {
                'signal': sentiment_signal.value,
                'articles_analyzed': len(sentiment_scores) if sentiment_scores else 0
            },
            'weights': weights,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Comprehensive signal for {ticker}: {final_signal.value}")
        return result
    
    @staticmethod
    def _signal_to_score(signal: Signal) -> float:
        """Convert signal to numeric score"""
        scores = {
            Signal.STRONG_BUY: 1.0,
            Signal.BUY: 0.5,
            Signal.HOLD: 0.0,
            Signal.SELL: -0.5,
            Signal.STRONG_SELL: -1.0
        }
        return scores.get(signal, 0.0)


# Example usage and testing
if __name__ == "__main__":
    logger.info("Initializing Comprehensive Signal Engine...")
    engine = ComprehensiveSignalEngine()
    
    # Test technical signals
    print("\n=== TECHNICAL SIGNAL GENERATION ===")
    tickers = ["AAPL", "MSFT", "GOOGL"]
    
    for ticker in tickers:
        technical_result = engine.technical_generator.generate_technical_signal(ticker)
        print(f"\n{ticker}:")
        print(f"  Signal: {technical_result.get('signal')}")
        print(f"  Price: ${technical_result.get('latest_price')}")
        print(f"  Change: {technical_result.get('price_change_percent')}%")
        print(f"  Individual Signals: {technical_result.get('individual_signals')}")
    
    # Test comprehensive signal
    print("\n=== COMPREHENSIVE SIGNAL GENERATION ===")
    
    # Mock sentiment scores
    mock_sentiment = [
        {'combined_sentiment': 'positive', 'combined_confidence': 0.85},
        {'combined_sentiment': 'positive', 'combined_confidence': 0.78},
        {'combined_sentiment': 'neutral', 'combined_confidence': 0.60},
    ]
    
    comprehensive = engine.generate_signal("AAPL", sentiment_scores=mock_sentiment)
    print(f"\nAPPL Final Signal: {comprehensive['final_signal']}")
    print(f"Combined Score: {comprehensive['combined_score']}")
    print(f"Technical Signal: {comprehensive['technical']['signal']}")
    print(f"Sentiment Signal: {comprehensive['sentiment']['signal']}")
    
    print("\n✅ Signal engine working!")
