import string

# Simulated datasets based on public opinion lexicons
HAPPY_WORDS = {
    "happy", "joy", "good", "great", "excellent", "awesome", "fantastic", 
    "smile", "laugh", "love", "beautiful", "wonderful", "delight", "glad", 
    "cheerful", "bright", "sunny", "blessed", "amused", "charmed", "ecstatic",
    "amazing", "perfect", "sweet", "brilliant", "yay", "hooray"
}

SAD_WORDS = {
    "sad", "sorrow", "bad", "terrible", "awful", "horrible", "cry", "tears", 
    "hate", "ugly", "depressed", "miserable", "grief", "pain", "hurt", 
    "angry", "mad", "upset", "heartbroken", "gloomy", "tragic", "disaster",
    "worst", "failure", "tragic", "devastated"
}

def number_happy(sentence):
    """Returns the number of happy words in the given sentence."""
    # Convert sentence to lowercase and remove punctuation
    clean_sentence = sentence.lower().translate(str.maketrans('', '', string.punctuation))
    words = clean_sentence.split()
    
    # Count how many words are in the HAPPY_WORDS dataset
    count = 0
    for word in words:
        if word in HAPPY_WORDS:
            count += 1
            
    return count

def number_sad(sentence):
    """Returns the number of sad words in the given sentence."""
    # Convert sentence to lowercase and remove punctuation
    clean_sentence = sentence.lower().translate(str.maketrans('', '', string.punctuation))
    words = clean_sentence.split()
    
    # Count how many words are in the SAD_WORDS dataset
    count = 0
    for word in words:
        if word in SAD_WORDS:
            count += 1
            
    return count

def main():
    # Ask the user for a string containing a sentence
    sentence = input("Enter a sentence: ")
    
    # Compute happiness and sadness levels
    happy_level = number_happy(sentence)
    sad_level = number_sad(sentence)
    
    # Print the counts
    print(f"\nHappy words: {happy_level}")
    print(f"Sad words: {sad_level}")
    
    # Determine and print the tone of the sentence
    if happy_level > sad_level:
        print("Analysis: Positive")
    elif sad_level > happy_level:
        print("Analysis: Negative")
    else:
        print("Analysis: Neutral")

# Run the program
if __name__ == "__main__":
    main()