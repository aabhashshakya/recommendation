from flask import Flask

app = Flask(__name__)


@app.route('/msg')
def get_msg():
    return {"hello": "world"}
