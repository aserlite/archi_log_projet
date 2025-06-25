from flask import request, jsonify, session, redirect, url_for
from db import mysql
from controllers.user import is_authenticated
from models.consumption import Consumption
from models.party import Party

def add_conso():
    if not is_authenticated():
        return jsonify({"success": False, "error": "Non authentifié"}), 401

    party_id = request.form.get("party_id")
    drink_id = request.form.get("drink_id")
    quantity = request.form.get("quantity", 1)
    comment = request.form.get("comment", "")
    user_id = session.get("user_id")

    if not party_id or not drink_id or not quantity:
        return jsonify({"success": False, "error": "Champs manquants"}), 400

    try:
        with mysql.connection.cursor() as cur:
            Consumption.create(cur, user_id, party_id, drink_id, quantity, comment)
            mysql.connection.commit()
            new_count = Party.count_user_drinks(cur, party_id, user_id)
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": True, "new_count": new_count})
        return redirect(url_for("view_party_route", party_id=party_id))
    except Exception as e:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": False, "error": str(e)}), 500
        return jsonify({"error": str(e)}), 500