from nlp.sentiment_analyzer import NewsArticleSentimentAnalyzer

analyzer = NewsArticleSentimentAnalyzer()

# Debug: Check individual scores
title_result = analyzer.analyze_article_title('Apple Beats Earnings')
print(f"Title scores: {title_result.scores}")

content_result = analyzer.analyze_article_content('Strong Q4 results')
print(f"Content scores: {content_result.scores}")

# Combined result
result = analyzer.analyze_article('Apple Beats Earnings', 'Strong Q4 results')
print(f"\nCombined sentiment: {result['combined_sentiment']}")
print(f"All scores: {result['all_scores']}")
