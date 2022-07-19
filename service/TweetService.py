import os
from flask import Flask
import tweepy
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get("TOKEN")
api = tweepy.Client(bearer_token=token, wait_on_rate_limit=True)


def getTweets(search_term):
    tweets = api.search_recent_tweets(query=search_term, max_results=100)
    tweet = tweets.data
    response = {}
    for i in range(len(tweet)):
        response[i] = tweet[i].text
    return response
