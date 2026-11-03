from textblob import TextBlob


# Initialize counters
positive = 0
neutral = 0
negative = 0


# Analyze 10 sentences
for i in range(10):
    print("\nSentence", i + 1)
    sentence = input("Enter a sentence: ")


    # Initialize TextBlob
    s = TextBlob(sentence)


    # Get sentiment polarity
    p = s.sentiment.polarity


    # Display polarity score
    print("Polarity:", p)


    # Determine sentiment
    if p < 0:
        print("Sentiment: Negative")
        negative += 1
    elif p == 0:
        print("Sentiment: Neutral")
        neutral += 1
    else:
        print("Sentiment: Positive")
        positive += 1


# Display summary
print("\nSENTIMENT SUMMARY")
print("Positive sentences:", positive)
print("Neutral sentences:", neutral)
print("Negative sentences:", negative)
print("Total sentences:", positive + neutral + negative)
