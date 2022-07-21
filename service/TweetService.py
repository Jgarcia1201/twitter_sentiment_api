import os
from flask import Flask
import tweepy
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get("TOKEN")
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_secret = os.environ.get("ACCESS_SECRET")

api = tweepy.Client(bearer_token=token,
                    consumer_key='2j1yUu89kx1DX8771HWuyTDEu',
                    consumer_secret='PngwBtqoBqSGsnFu3hZHMd1MklG27ndfPKjNeLVSyUNbUryHzy',
                    access_token='1547040810717388800-p0yFvVEofxvbxK3TrNxYrWffBe0hdK',
                    access_token_secret='580eDdQJhSxUUiC3gi8wbS6IGulXmRN4mjcpeXeyB2u6D')


def getTweets(search_term):
    tweets = api.search_recent_tweets(query=search_term, max_results=100, user_auth=True)
    tweet = tweets.data
    response = {}
    for i in range(len(tweet)):
        response[i] = tweet[i].text
    return response
