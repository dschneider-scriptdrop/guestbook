from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello Docker + Nginx + Gunicorn + Flask!'
