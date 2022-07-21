import pickle
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('omw-1.4')


def processTweets(tweets):
    response = {}
    labels = ["Text"]
    df = pd.DataFrame.from_dict(tweets, orient='index', columns=labels)
    df = df.drop_duplicates()
    df["Text"] = df["Text"].str.replace("/d", "")
    df["Text"] = df["Text"].str.replace("RT", "")
    df["Text"] = df["Text"].str.replace("im", "")
    df["Text"] = df["Text"].str.replace("http", "")
    df["Text"] = df["Text"].apply(tweet_cleaner)

    word_counts = pd.Series(" ".join(df["Text"]).split()).value_counts()
    uncommon_words = word_counts[word_counts <= 2]
    df["Text"] = df["Text"].apply(lambda j: " ".join([i for i in j.split() if i not in uncommon_words]))

    vectorizer = pickle.load(open('./ml/twt_sentiment_vectorizer', 'rb'))
    vectorized_tweets = vectorizer.transform(df["Text"])

    nb_model = pickle.load(open("./ml/twt_sentiment_nb_model", 'rb'))
    nb_prediction = nb_model.predict(vectorized_tweets)
    ml_response = calculateSentiment(nb_prediction)

    word_counts_packaged = packageCounts(word_counts[0:50].to_dict())

    response["word_counts"] = word_counts_packaged
    response["sentiment"] = ml_response

    return response


def tweet_cleaner(data):
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(str(data).replace("`", "").lower())
    removed_punctuation = [i for i in tokens if i.isalpha()]
    removed_stopwords = [i for i in removed_punctuation if i not in stop_words]
    lemmatized_words = [WordNetLemmatizer().lemmatize(i) for i in removed_stopwords]
    text_cleaned = [PorterStemmer().stem(i) for i in lemmatized_words]
    return " ".join(text_cleaned)


def calculateSentiment(data):
    sentiment_score = 0
    sentiment_divisor = 0
    positive = 0
    neutral = 0
    negative = 0

    print(len(data))

    for point in data:
        if point == 1:
            positive += 1
            sentiment_score += 1
            sentiment_divisor += 1
        elif point == -1:
            negative += 1
            sentiment_score -= 1
            sentiment_divisor += 1
        else:
            neutral += 1

    if sentiment_divisor > 0:
        sentiment_score = sentiment_score / sentiment_divisor

    return {
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "score": sentiment_score
    }


def packageCounts(counts):
    to_return = []
    key_list = list(counts.keys())
    val_list = list(counts.values())
    for i in range(len(counts)):
        temp = {"value": key_list[i], "count": val_list[i]}
        to_return.append(temp)
    return to_return
