from flask import Blueprint
from repository.TweetRepo import processTweets
from service.TweetService import getTweets
from flask_cors import cross_origin

tweet_controller = Blueprint('tweet_controller', __name__)


@tweet_controller.route('/<search_term>')
@cross_origin(origins="http://localhost:3000")
def demo(search_term):
    tweets = getTweets(search_term)
    return processTweets(tweets)
