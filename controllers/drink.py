from flask import jsonify
from models.drink import Drink
from db import mysql

def get_all_drinks():
    try:
        with mysql.connection.cursor() as cur:
            drinks = Drink.get_all(cur)
        drinks_list = [drink.__dict__ for drink in drinks]
        return jsonify(drinks_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

