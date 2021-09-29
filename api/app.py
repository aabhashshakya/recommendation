from flask import Flask
import pandas as pd

app = Flask(__name__)


@app.route('/msg')
def get_msg():
    return {"hello": "world"}


@app.route('/getbooklist')
def getbooklist():
    store_data = pd.read_csv('Books.csv')
    store_data = store_data.head(2)
    json_data = store_data.to_json(orient='index')
    return json_data
