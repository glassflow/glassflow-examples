import json


def handler(data, log):
    log.info("Event:" + json.dumps(data), data=data)

    text = data["text"].lower()  # Convert text to lowercase to simplify comparisons

    # Lists of positive and negative keywords
    positive_keywords = ['happy', 'joy', 'love', 'wonderful', 'fantastic', 'good', 'great', 'excellent']
    negative_keywords = ['sad', 'bad', 'hate', 'terrible', 'horrible', 'poor', 'worst', 'awful']

    # Count occurrences of positive and negative keywords
    positive_count = sum(text.count(word) for word in positive_keywords)
    negative_count = sum(text.count(word) for word in negative_keywords)

    # Determine sentiment based on the counts
    if positive_count > negative_count:
        sentiment = "positive"
    elif negative_count > positive_count:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    data["sentiment"] = sentiment
    return data