import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import json
# Download the VADER lexicon used by the SentimentIntensityAnalyzer
nltk.download('vader_lexicon')


# Additional keywords for classifying sentiment

with open("reviews.json","r") as file:
    reviews = json.load(file)

sia = SentimentIntensityAnalyzer()


def classify_sentiment(sentiment_score):
    if sentiment_score >= 0.4:
        return "Positive"
    elif sentiment_score <= -0.4:
        return "Negative"
    else:
        return "Mixed"
    
# Function to perform sentiment analysis on each review
def perform_sentiment_analysis(review):
    sentiment_score = sia.polarity_scores(review["review_body"])["compound"]
    
    if sentiment_score >= 0.4:
        sentiment_label = "Positive"
    elif sentiment_score <= -0.4:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Mixed"

    return sentiment_label, sentiment_score    

def normalize_review_sentiment(value):
    min_x = -1
    max_x = 1
    min_new = 1
    max_new = 5
    
    normalized_value = ((value - min_x) / (max_x - min_x)) * (max_new - min_new) + min_new
    return normalized_value

total_sentiment_score = 0
num_reviews = len(reviews)

# Perform sentiment analysis on each review
for review in reviews:  
    sentiment_label, sentiment_score = perform_sentiment_analysis(review)
    title_sentiment_score = sia.polarity_scores(review["review_title"])["compound"]
    total_sentiment_score += sentiment_score
'''
    print(title_sentiment_score)
    print("Review Title:", review["review_title"])
    print("Review Title Sentiment:", title_sentiment)
    print("Review Sentiment Label:", sentiment_label)
    print("Review Sentiment Score:", sentiment_score)
    print("---")
'''
average_sentiment_score = total_sentiment_score / num_reviews
# Print aggregated sentiment information
print("Average Review Sentiment Score:", round(average_sentiment_score,4))
print("Normalized Score: ",normalize_review_sentiment(round(average_sentiment_score,4)))


