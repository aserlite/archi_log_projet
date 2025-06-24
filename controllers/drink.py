from flask import jsonify, request, redirect, url_for
from models.drink import Drink
from db import mysql
from flask import render_template


def get_all_drinks():
    try:
        with mysql.connection.cursor() as cur:
            drinks = Drink.get_all(cur)
            drinks_list = [drink.__dict__ for drink in drinks]
        return render_template('drinks/drinks.html', drinks=drinks_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def create_drink():
    try:
        with mysql.connection.cursor() as cur:
            nom = request.form.get("nom")
            ingredients = request.form.get("ingredients")
            alcool = request.form.get("alcool", "on") == "on"
            degre = request.form.get("degre")
            description = request.form.get("description")
            drink_id = Drink.create(cur, nom, ingredients, alcool, degre, description)
            mysql.connection.commit()
        return redirect(url_for('single_drink_route', drink_id=drink_id))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def single_drink(drink_id):
    try:
        with mysql.connection.cursor() as cur:
            drink = Drink.get_by_id(cur, drink_id)
            if not drink:
                return jsonify({"error": "Drink not found"}), 404
            return render_template('drinks/single.html', drink=drink.__dict__)
    except Exception as e:
        return jsonify({"error": str(e)}), 500