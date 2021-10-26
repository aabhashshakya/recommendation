import pandas as pd
from flask import Flask, request, json, jsonify, Blueprint
from flask.wrappers import Request, Response

books = Blueprint('books', __name__) #blueprint basically tells that this file is part of the app
#it helps in modularizing our app so that all code is not in a single file ok

@books.route('/getbooklist')
def getbooklist():
    store_data = pd.read_csv('api/Books.csv')
    store_data = store_data.head(2)
    return store_data.to_dict(orient="index")#same as to_Json but is compatible with JsonViewerPro in chrome
    


@books.route('/searchbook', methods=["POST"])
def searchbook():
    request_data = request.get_json()
    return {"result": request_data}
