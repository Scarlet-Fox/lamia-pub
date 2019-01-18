# License header will go here when I pick one.

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
