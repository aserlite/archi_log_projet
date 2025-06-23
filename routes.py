from app_instance import app
from db import mysql
from flask import jsonify
from flask import render_template
from controllers.drink import *
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/drinks")
def drinks():
    return get_all_drinks()
