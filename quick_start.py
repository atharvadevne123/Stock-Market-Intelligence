#!/usr/bin/env python3
"""
Stock Market Intelligence - Quick Start Guide
Run this script to get started immediately with the system
"""

import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_environment():
    """Check if all dependencies are installed"""
    print("=" * 80)
    print("CHECKING ENVIRONMENT")
    print("=" * 80)
    
    required_packages = [
        'requests',
        'beautifulsoup4',
        'feedparser',
        'pandas',
        'yfinance',
        'transformers',
        'torch',
        'fastapi',
        'sqlalchemy',
        'praw'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False
    
    print("\n✅ All dependencies installed!")
    return True


def quick_analysis():
    """Run a quick analysis to verify everything works"""
    print("\n" + "=" * 80)
    print("QUICK ANALYSIS TEST")
    print("=" * 80)
    
    try:
        # Import modules
        print("\nImporting modules...")
        from news_scraper import NewsAggregator
        from sentiment_analyzer import NewsArticleSentimentAnalyzer
        from signal_engine import ComprehensiveSignalEngine
        
        print("✅ All modules imported successfully\n")
        
        # Initialize components
        print("Initializing components...")
        news_agg = NewsAggregator()
        sentiment = NewsArticleSentimentAnalyzer()
        signal_engine = ComprehensiveSignalEngine()
        print("✅ Components initialized\n")
        
        # Test news scraping
        print("Testing news scraping (AAPL)...")
        articles = news_agg.get_ticker_news("AAPL", hours=24)
        print(f"✅ Found {len(articles)} articles\n")
        
        if articles:
            # Test sentiment analysis
            print("Testing sentiment analysis...")
            article = articles[0]
            sentiment_result = sentiment.analyze_article(
                title=article.title,
                content=article.content
            )
            print(f"✅ Article sentiment: {sentiment_result['combined_sentiment']}\n")
        
        # Test technical analysis
        print("Testing technical analysis (AAPL)...")
        technical = signal_engine.technical_generator.generate_technical_signal("AAPL")
        print(f"✅ Technical signal: {technical.get('signal')}\n")
        
        # Test comprehensive signal
        print("Testing comprehensive signal generation...")
        signal = signal_engine.generate_signal("AAPL")
        print(f"✅ Final signal: {signal['final_signal']}\n")
        
        print("=" * 80)
        print("✅ QUICK TEST PASSED - SYSTEM IS WORKING!")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"\n❌ Error during quick test: {e}")
        import traceback
        traceback.print_exc()
        return False


def example_usage():
    """Show example usage patterns"""
    print("\n" + "=" * 80)
    print("EXAMPLE USAGE PATTERNS")
    print("=" * 80)
    
    examples = """
1. SINGLE TICKER ANALYSIS
   ═══════════════════════════════════════════════════════════════════════════
   
   from main_orchestrator import StockMarketIntelligence
   
   system = StockMarketIntelligence()
   analysis = system.analyze_ticker("AAPL", hours=24)
   
   print(f"Signal: {analysis['signal']['final_signal']}")
   print(f"Price: ${analysis['signal']['technical']['latest_price']}")
   

2. PORTFOLIO ANALYSIS
   ═══════════════════════════════════════════════════════════════════════════
   
   tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
   portfolio = system.analyze_portfolio(tickers)
   
   print(f"Recommendation: {portfolio['summary']['recommendation']}")
   print(f"Signals: {portfolio['summary']['signal_distribution']}")
   

3. MARKET OVERVIEW
   ═══════════════════════════════════════════════════════════════════════════
   
   market = system.get_market_overview(hours=24)
   
   print(f"Trend: {market['market_trend']}")
   print(f"Sentiment: {market['sentiment_ratios']}")
   

4. NEWS SCRAPING
   ═══════════════════════════════════════════════════════════════════════════
   
   from scraper.news_scraper import NewsAggregator
   
   aggregator = NewsAggregator()
   articles = aggregator.get_market_news(hours=24)
   
   for article in articles[:5]:
       print(f"{article.title} ({article.source})")
   

5. SENTIMENT ANALYSIS
   ═══════════════════════════════════════════════════════════════════════════
   
   from nlp.sentiment_analyzer import NewsArticleSentimentAnalyzer
   
   analyzer = NewsArticleSentimentAnalyzer()
   result = analyzer.analyze_article(
       title="Stock Surges on Earnings",
       content="Company reported strong Q4 results..."
   )
   
   print(f"Sentiment: {result['combined_sentiment']}")
   print(f"Confidence: {result['combined_confidence']}")
   

6. TECHNICAL ANALYSIS
   ═══════════════════════════════════════════════════════════════════════════
   
   from analysis.signal_engine import TechnicalSignalGenerator
   
   gen = TechnicalSignalGenerator()
   signal = gen.generate_technical_signal("MSFT")
   
   print(f"Signal: {signal['signal']}")
   print(f"Technical Data: {signal['technical_data']}")
    """
    
    print(examples)


def show_api_examples():
    """Show FastAPI examples"""
    print("\n" + "=" * 80)
    print("FASTAPI USAGE (Once Backend is Running)")
    print("=" * 80)
    
    api_info = """
Start the API server:
  python api/main.py

API will be available at: http://localhost:8000
API documentation at: http://localhost:8000/docs

EXAMPLE REQUESTS:
═══════════════════════════════════════════════════════════════════════════

1. Analyze Single Ticker:
   GET http://localhost:8000/api/analyze/AAPL
   
   Response:
   {
     "ticker": "AAPL",
     "final_signal": "BUY",
     "combined_score": 0.654,
     "technical": { ... },
     "sentiment": { ... }
   }

2. Portfolio Analysis:
   GET http://localhost:8000/api/portfolio?tickers=AAPL,MSFT,GOOGL
   
   Response:
   {
     "portfolio": ["AAPL", "MSFT", "GOOGL"],
     "recommendation": "BULLISH",
     "signals": { "BUY": 2, "HOLD": 1, "SELL": 0 }
   }

3. Market Overview:
   GET http://localhost:8000/api/market/overview
   
   Response:
   {
     "market_trend": "BULLISH",
     "sentiment_ratios": { "positive": 0.62, "negative": 0.18 },
     "articles_analyzed": 150
   }

4. Technical Indicators:
   GET http://localhost:8000/api/technical/AAPL
   
   Response:
   {
     "ticker": "AAPL",
     "rsi": 65.4,
     "macd": { ... },
     "bollinger_bands": { ... },
     "moving_averages": { ... }
   }

5. Sentiment Analysis:
   GET http://localhost:8000/api/sentiment/AAPL
   
   Response:
   {
     "ticker": "AAPL",
     "positive_ratio": 0.65,
     "negative_ratio": 0.15,
     "trend": "BULLISH"
   }
    """
    
    print(api_info)


def main():
    """Main entry point"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "STOCK MARKET INTELLIGENCE - QUICK START GUIDE".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # Check environment
    if not check_environment():
        print("\n⚠️  Please install missing dependencies first!")
        return False
    
    # Run quick test
    test_choice = input("\n\nRun quick functionality test? (y/n): ").lower()
    if test_choice == 'y':
        if not quick_analysis():
            print("\n⚠️  Quick test failed. Check the errors above.")
            return False
    
    # Show examples
    show_examples = input("\nShow example usage patterns? (y/n): ").lower()
    if show_examples == 'y':
        example_usage()
    
    # Show API info
    show_api = input("\nShow API usage examples? (y/n): ").lower()
    if show_api == 'y':
        show_api_examples()
    
    # Next steps
    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    
    next_steps = """
1. START THE MAIN ORCHESTRATOR:
   python main_orchestrator.py

2. START THE API SERVER:
   python api/main.py
   
3. START THE FRONTEND (in separate terminal):
   cd frontend
   npm install
   npm start

4. CONFIGURE DATABASE (if needed):
   - Edit .env with your PostgreSQL credentials
   - Run: alembic upgrade head

5. SET UP SCHEDULING (for continuous updates):
   - Configure Celery in scheduler/celery_config.py
   - Run: celery -A scheduler.tasks worker

USEFUL COMMANDS:
═════════════════════════════════════════════════════════════════════════════

# Analyze a single stock
python -c "from main_orchestrator import StockMarketIntelligence; \\
system = StockMarketIntelligence(); \\
print(system.analyze_ticker('AAPL')['signal']['final_signal'])"

# Analyze multiple stocks
python -c "from main_orchestrator import StockMarketIntelligence; \\
system = StockMarketIntelligence(); \\
result = system.analyze_portfolio(['AAPL', 'MSFT', 'GOOGL']); \\
print(result['summary']['recommendation'])"

# Get market overview
python -c "from main_orchestrator import StockMarketIntelligence; \\
system = StockMarketIntelligence(); \\
market = system.get_market_overview(); \\
print(f'Market Trend: {market[\"market_trend\"]}')"

DOCUMENTATION:
═════════════════════════════════════════════════════════════════════════════
- README.md           : Comprehensive project documentation
- .env.example        : Environment variables template
- api/main.py         : API endpoint documentation
- scraper/            : News scraping modules
- nlp/                : Sentiment analysis modules
- analysis/           : Signal generation modules

TROUBLESHOOTING:
═════════════════════════════════════════════════════════════════════════════
If you encounter issues:

1. Check Python version: python --version (requires 3.9+)
2. Verify dependencies: pip list | grep -E "pandas|torch|transformers"
3. Check .env file: cat .env
4. Review logs for errors
5. Test individual modules separately

For more help, see README.md or open an issue on GitHub.
    """
    
    print(next_steps)
    
    print("\n" + "=" * 80)
    print("✅ YOU'RE ALL SET! START USING STOCK MARKET INTELLIGENCE!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
