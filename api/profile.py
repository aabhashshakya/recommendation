from flask import jsonify, Blueprint, request
from flask_login import current_user, login_required

from __init__ import db
from flask_jwt_extended import jwt_required


profile = Blueprint('profile', __name__) #blueprint basically tells that this file is part of the app
#it helps in modularizing our app so that all code is not in a single file

@profile.route('/purchasehistory', methods = ["GET"])
@login_required
@jwt_required()
def getPurchaseHistory():
    try:
        purchasedBookList = current_user.purchased_books #this will give a list of PurchaseHistory objects
        #this list cannot be converted to JSON directly, so we need to do below things
        if(purchasedBookList):
            purchasedBookListJson=[]
            for book in purchasedBookList:
                purchasedBookListJson.append(book.to_dict()) #converting each PurchaseHistory table object to JSON
                return jsonify(orders = purchasedBookListJson, orders_count=len(purchasedBookListJson)), 200
        return jsonify(orders_count=0), 200
    except:
        return jsonify(msg="Some error occured during getting the purchase history. Try again."), 500
        

    
@profile.route('/buybook', methods = ["POST"])
@login_required
@jwt_required()
def buy():
    from models.modelbase import PurchaseHistory
    try:
        requestData = request.get_json()
        book_isbn = requestData.get('book_isbn')
        book_name = requestData.get('book_name')
        count = requestData.get('count')       
        book = PurchaseHistory(book_isbn=book_isbn,book_name=book_name,count=count,user_id=current_user.id)
        db.session.add(book)
        db.session.commit()    
        return jsonify(msg = "Book purchase successful", ), 200
    except:
        return jsonify(msg="Some error occured during purchase. Try again."), 500