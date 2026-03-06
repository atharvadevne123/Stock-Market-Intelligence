"""
Main Orchestrator for Stock Market Intelligence
Integrates news scraper, sentiment analyzer, and signal engine
"""

import logging
import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StockMarketIntelligence:
    """Main orchestrator class"""
    
    def __init__(self):
        """Initialize all components"""
        logger.info("Initializing Stock Market Intelligence System...")
        
        try:
            # Import components
            from scraper.news_scraper import NewsAggregator
            from nlp.sentiment_analyzer import NewsArticleSentimentAnalyzer
            from analysis.signal_engine import ComprehensiveSignalEngine
            
            self.news_aggregator = NewsAggregator()
            self.sentiment_analyzer = NewsArticleSentimentAnalyzer()
            self.signal_engine = ComprehensiveSignalEngine()
            
            logger.info("✅ All components initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            raise
    
    def analyze_ticker(self, ticker: str, hours: int = 24) -> Dict:
        """
        Perform complete analysis for a ticker
        
        Args:
            ticker: Stock ticker symbol (e.g., "AAPL")
            hours: Hours of news to analyze
            
        Returns:
            Comprehensive analysis with signals and recommendations
        """
        logger.info(f"Starting comprehensive analysis for {ticker}...")
        
        result = {
            'ticker': ticker,
            'timestamp': datetime.now().isoformat(),
            'analysis_steps': []
        }
        
        try:
            # Step 1: Get news
            logger.info(f"Step 1: Fetching news for {ticker}...")
            articles = self.news_aggregator.get_ticker_news(ticker, hours=hours)
            
            result['news'] = {
                'articles_found': len(articles),
                'articles': [article.to_dict() for article in articles[:5]]  # Top 5
            }
            result['analysis_steps'].append("✅ News fetching complete")
            
            # Step 2: Analyze sentiment
            logger.info(f"Step 2: Analyzing sentiment from {len(articles)} articles...")
            sentiment_results = []
            
            for article in articles[:10]:  # Analyze top 10 articles
                sentiment = self.sentiment_analyzer.analyze_article(
                    title=article.title,
                    content=article.content
                )
                sentiment_results.append(sentiment)
            
            result['sentiment'] = {
                'articles_analyzed': len(sentiment_results),
                'results': sentiment_results[:3]  # Top 3
            }
            result['analysis_steps'].append("✅ Sentiment analysis complete")
            
            # Step 3: Generate trading signal
            logger.info(f"Step 3: Generating trading signal...")
            signal = self.signal_engine.generate_signal(
                ticker,
                sentiment_scores=sentiment_results
            )
            
            result['signal'] = signal
            result['analysis_steps'].append("✅ Signal generation complete")
            
            logger.info(f"Analysis complete for {ticker}: {signal['final_signal']}")
            
        except Exception as e:
            logger.error(f"Error during analysis: {e}")
            result['error'] = str(e)
        
        return result
    
    def analyze_portfolio(self, tickers: List[str], hours: int = 24) -> Dict:
        """
        Analyze multiple tickers at once
        
        Args:
            tickers: List of stock ticker symbols
            hours: Hours of news to analyze
            
        Returns:
            Analysis results for all tickers
        """
        logger.info(f"Analyzing portfolio of {len(tickers)} tickers...")
        
        results = {
            'portfolio': tickers,
            'timestamp': datetime.now().isoformat(),
            'analyses': [],
            'summary': {}
        }
        
        for i, ticker in enumerate(tickers, 1):
            logger.info(f"Analyzing {ticker} ({i}/{len(tickers)})...")
            analysis = self.analyze_ticker(ticker, hours=hours)
            results['analyses'].append(analysis)
        
        # Generate portfolio summary
        results['summary'] = self._generate_portfolio_summary(results['analyses'])
        
        logger.info(f"Portfolio analysis complete")
        return results
    
    def _generate_portfolio_summary(self, analyses: List[Dict]) -> Dict:
        """Generate summary statistics for portfolio"""
        signal_counts = {
            'STRONG_BUY': 0,
            'BUY': 0,
            'HOLD': 0,
            'SELL': 0,
            'STRONG_SELL': 0
        }
        
        for analysis in analyses:
            if 'signal' in analysis and 'final_signal' in analysis['signal']:
                signal = analysis['signal']['final_signal']
                if signal in signal_counts:
                    signal_counts[signal] += 1
        
        return {
            'total_analyzed': len(analyses),
            'signal_distribution': signal_counts,
            'recommendation': self._get_portfolio_recommendation(signal_counts)
        }
    
    @staticmethod
    def _get_portfolio_recommendation(signal_counts: Dict) -> str:
        """Get overall portfolio recommendation"""
        buy_signals = signal_counts['STRONG_BUY'] + signal_counts['BUY']
        sell_signals = signal_counts['STRONG_SELL'] + signal_counts['SELL']
        
        if buy_signals > sell_signals + 1:
            return "BULLISH"
        elif sell_signals > buy_signals + 1:
            return "BEARISH"
        else:
            return "NEUTRAL"
    
    def get_market_overview(self, hours: int = 24) -> Dict:
        """
        Get overall market sentiment and trends
        
        Args:
            hours: Hours of news to analyze
            
        Returns:
            Market overview with sentiment trends
        """
        logger.info("Generating market overview...")
        
        try:
            # Get general market news
            market_news = self.news_aggregator.get_market_news(hours=hours)
            
            # Analyze sentiment of market news
            sentiment_results = []
            for article in market_news[:20]:  # Analyze top 20
                try:
                    sentiment = self.sentiment_analyzer.analyze_article(
                        title=article.title,
                        content=article.content
                    )
                    sentiment_results.append(sentiment)
                except:
                    pass
            
            # Calculate aggregated sentiment
            positive = sum(1 for s in sentiment_results 
                         if s.get('combined_sentiment') == 'positive')
            negative = sum(1 for s in sentiment_results 
                         if s.get('combined_sentiment') == 'negative')
            neutral = sum(1 for s in sentiment_results 
                        if s.get('combined_sentiment') == 'neutral')
            
            total = len(sentiment_results)
            
            result = {
                'timestamp': datetime.now().isoformat(),
                'articles_analyzed': total,
                'sentiment_distribution': {
                    'positive': positive,
                    'negative': negative,
                    'neutral': neutral
                },
                'sentiment_ratios': {
                    'positive': round(positive / total, 3) if total > 0 else 0,
                    'negative': round(negative / total, 3) if total > 0 else 0,
                    'neutral': round(neutral / total, 3) if total > 0 else 0
                },
                'market_trend': self._determine_market_trend(positive, negative, neutral),
                'top_sources': self._get_top_sources(market_news)
            }
            
            logger.info(f"Market trend: {result['market_trend']}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating market overview: {e}")
            return {'error': str(e)}
    
    @staticmethod
    def _determine_market_trend(positive: int, negative: int, neutral: int) -> str:
        """Determine market trend from sentiment"""
        total = positive + negative + neutral
        if total == 0:
            return "UNKNOWN"
        
        pos_ratio = positive / total
        neg_ratio = negative / total
        
        if pos_ratio > 0.55:
            return "BULLISH"
        elif neg_ratio > 0.55:
            return "BEARISH"
        else:
            return "NEUTRAL"
    
    @staticmethod
    def _get_top_sources(articles: List) -> List[str]:
        """Get most common news sources"""
        sources = {}
        for article in articles:
            source = article.source
            sources[source] = sources.get(source, 0) + 1
        
        # Return top 5 sources
        sorted_sources = sorted(sources.items(), key=lambda x: x[1], reverse=True)
        return [source for source, count in sorted_sources[:5]]
    
    def export_analysis(self, analysis: Dict, filename: str):
        """Export analysis results to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(analysis, f, indent=2, default=str)
            logger.info(f"Analysis exported to {filename}")
        except Exception as e:
            logger.error(f"Error exporting analysis: {e}")


# Example usage
if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("STOCK MARKET INTELLIGENCE SYSTEM")
    logger.info("=" * 80)
    
    try:
        # Initialize system
        system = StockMarketIntelligence()
        
        # Single ticker analysis
        print("\n" + "=" * 80)
        print("SINGLE TICKER ANALYSIS (AAPL)")
        print("=" * 80)
        
        single_analysis = system.analyze_ticker("AAPL", hours=24)
        print(f"\nTicket: {single_analysis['ticker']}")
        print(f"Final Signal: {single_analysis['signal']['final_signal']}")
        print(f"Combined Score: {single_analysis['signal']['combined_score']}")
        print(f"Articles Analyzed: {single_analysis['news']['articles_found']}")
        
        # Portfolio analysis
        print("\n" + "=" * 80)
        print("PORTFOLIO ANALYSIS")
        print("=" * 80)
        
        portfolio_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
        portfolio_analysis = system.analyze_portfolio(portfolio_tickers, hours=24)
        
        print(f"\nPortfolio: {portfolio_tickers}")
        print(f"Overall Recommendation: {portfolio_analysis['summary']['recommendation']}")
        print(f"Signal Distribution: {portfolio_analysis['summary']['signal_distribution']}")
        
        # Market overview
        print("\n" + "=" * 80)
        print("MARKET OVERVIEW")
        print("=" * 80)
        
        market_overview = system.get_market_overview(hours=24)
        print(f"\nMarket Trend: {market_overview['market_trend']}")
        print(f"Articles Analyzed: {market_overview['articles_analyzed']}")
        print(f"Sentiment Distribution: {market_overview['sentiment_distribution']}")
        print(f"Top Sources: {market_overview['top_sources']}")
        
        # Export results
        system.export_analysis(portfolio_analysis, "portfolio_analysis.json")
        system.export_analysis(market_overview, "market_overview.json")
        
        print("\n" + "=" * 80)
        print("✅ ANALYSIS COMPLETE")
        print("=" * 80)
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
