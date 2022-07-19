from flask import Flask
from controller.TweetController import tweet_controller

app = Flask(__name__)

# ROUTES
app.register_blueprint(tweet_controller, url_prefix="/search")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
