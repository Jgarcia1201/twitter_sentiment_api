from flask import Blueprint
from repository.TweetRepo import processTweets
from service.TweetService import getTweets

tweet_controller = Blueprint('tweet_controller', __name__)


@tweet_controller.route('/<search_term>')
def demo(search_term):
    tweets = getTweets(search_term)
    return processTweets(tweets)
