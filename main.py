from flask import Flask
from controller.TweetController import tweet_controller
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

# ROUTES
app.register_blueprint(tweet_controller, url_prefix="/search")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
