from flask import json, jsonify, Blueprint, request
from flask_login import current_user, login_required
from sqlalchemy.orm import session

from __init__ import db
from flask_jwt_extended import jwt_required
from __init__ import store_data_uncleaned
from models.modelbase import CartItem, PurchasedItem


profile = Blueprint('profile', __name__) #blueprint basically tells that this file is part of the app
#it helps in modularizing our app so that all code is not in a single file
    
@profile.route('/addtocart', methods = ["POST"])
@login_required
@jwt_required()
def addToCart():
    try:
        bookisbn_ = request.get_json().get('isbn')
        bookcount = request.get_json().get('count')
        existingCartItem = CartItem.query.filter_by(book_isbn = bookisbn_).first()
        if(existingCartItem): #if item is in cart, just increment count
            existingCartItem.count = CartItem.count + bookcount
            db.session.commit()
            return jsonify(bookisbn = bookisbn_, count = existingCartItem.count, msg="Updated the cart item"), 200
        #if item not in cart # add it to cart
        cartItem = CartItem(book_isbn = bookisbn_, count = bookcount, user_id = current_user.id)
        db.session.add(cartItem)
        db.session.commit()
        return jsonify(bookisbn = bookisbn_, count = bookcount, msg="Added the cart item"), 200
    except Exception as e:
        print(e)
        return jsonify(msg="Failed to add/update the cart item", errmsg = str(e)), 500   
    
    
@profile.route('/cart', methods = ["GET"])
@login_required
@jwt_required()
def getCart():
    try:
        cart = current_user.cart
        if(cart):
            cartJson=[]
            for cartItem in cart:
                #check if the item in cart is in the csv file.
                book = store_data_uncleaned[store_data_uncleaned["isbn"] == cartItem.book_isbn]
                #if yes return the full book details
                if(not book.empty):#always check if the dataframe is empty like this
                    book['count'] = cartItem.count
                    book['date'] = cartItem.date
                    book_dict = book.to_dict(orient='index')
                    cartJson.append(book_dict) 
            return jsonify(cart = cartJson, cartitem_count=len(cartJson)), 200
        #if cart empty return null
        return jsonify(cart = None, cartitem_count=0), 200 #none = null
    except Exception as e:
        print(e)
        return jsonify(msg="Some error occured during getting the cart. Try again.",
                       errmsg = str(e)), 500

    
@profile.route('/buybook', methods = ["POST"])
@login_required
@jwt_required()
def buy():
    try:
        requestData = request.get_json()
        bookisbn_ = requestData.get('isbn')
        bookcount = requestData.get('count') 
         #check if the item to buy is in the csv file.
        bookToBuy = store_data_uncleaned[store_data_uncleaned["isbn"] == bookisbn_]
        if( not bookToBuy.empty):
            book = PurchasedItem(book_isbn=bookisbn_,count=bookcount,user_id=current_user.id)
            db.session.add(book)
            db.session.commit()    
            return jsonify(msg = "Book purchase successful", bookisbn = bookisbn_, count = bookcount), 200
        else:
            return jsonify(msg = "Book purchase failed", errmsg = "Book not in the store. Wrong isbn"), 400
    except Exception as e:
        print(e)
        return jsonify(msg="Some error occured during purchase. Try again.", errmsg = str(e)), 500
    
@profile.route('/purchasehistory', methods = ["GET"])
@login_required
@jwt_required()
def getPurchaseHistory():
    try:
        purchasedItemsList= current_user.purchased_books
        if(purchasedItemsList):
            purchasedItemsJson=[]
            for purchasedItem in purchasedItemsList:
                book = store_data_uncleaned[store_data_uncleaned["isbn"] == purchasedItem.book_isbn]
                if(not book.empty):
                    book['count'] = purchasedItem.count
                    book['date'] = purchasedItem.date
                    book_dict = book.to_dict(orient='index')
                    purchasedItemsJson.append(book_dict) 
            return jsonify(purchasedItems = purchasedItemsJson, purchase_count=len(purchasedItemsJson)), 200
        return jsonify(purchasedItem = None, purchase_count=0), 200
    except Exception as e:
        print(e)
        return jsonify(msg="Some error occured during getting the purchase history. Try again.",
                       errmsg = str(e)), 500