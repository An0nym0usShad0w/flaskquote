import pymongo
from flask import Flask, redirect, url_for, render_template, request
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

MONGO_URL = os.getenv("MONGO_URL")

cluster = MongoClient(MONGO_URL)
cluster_db = cluster["flaskquotes"]
quote_collection = cluster_db["quotes"]

#sorted by date

app = Flask(__name__)
app.debug = True

@app.route('/')
def home():
    sorted_quote_collection = quote_collection.find().sort('time_posted', pymongo.DESCENDING)
    return render_template('home.html', title = 'home', quote_posts = sorted_quote_collection)

@app.route("/enterquote", methods=["POST", "GET"])
def enter_quote():
    if request.method == "POST":
        author = request.form["author"]
        quote = request.form["quote"]

        quote_collection.insert_one({'author' : author, 'time_posted': datetime.now(), 'quote': quote})
        print('author:', author, 'quote:', quote)
        return redirect(url_for("home"))
    else:
        return render_template("quote_enter.html", title='Enter Quote')

@app.route('/about')
def about_page():
    return render_template("about.html", title='About')

app.run()
