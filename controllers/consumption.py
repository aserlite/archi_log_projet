from flask import request, jsonify, session, redirect, url_for
from db import mysql
from controllers.user import is_authenticated
from models.consumption import Consumption
from models.party import Party
from models.user import User
from datetime import datetime


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
            pseudo = User.get_pseudo_by_id(cur, user_id)
            new_count = Party.count_user_drinks(cur, party_id, user_id)
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": True, "id":user_id, "new_count": new_count, "pseudo": pseudo}), 200
        return redirect(url_for("view_party_route", party_id=party_id))
    except Exception as e:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": False, "error": str(e)}), 500
        return jsonify({"error": str(e)}), 500


def calculer_taux_alcoolemie(alcoolique):
    instant_T = datetime.now()
    dose_alcool = 10
    elimination = 0.15

    if not session.get("user_id"):
        return jsonify({"taux": 0})
    party_id = is_user_in_party();
    if not party_id:
        return jsonify({"taux": 0})
    cursor = mysql.connection.cursor()
    user = User.get_by_id(cursor, alcoolique)
    if not user:
        return jsonify({"taux": 0})

    poids = user.poids
    genre = user.genre
    coef = 0.7 if genre == 'Homme' else 0.6

    consommations = Consumption.get_consumption_by_user_by_party(cursor, session.get("user_id"), party_id)
    alcool_total = 0
    for conso in consommations:
        if isinstance(conso.timestamp, str):
            conso_time = datetime.fromisoformat(conso.timestamp)
        else:
            conso_time = conso.timestamp
        heures_ecoulees = (instant_T - conso_time).total_seconds() / 3600
        if heures_ecoulees < 0:
            continue
        alcool_restant = dose_alcool * conso.quantité - elimination * heures_ecoulees
        if alcool_restant > 0:
            alcool_total += alcool_restant

    taux = alcool_total / (float(poids) * float(coef)) if poids and coef else 0
    taux = max(taux, 0)
    taux = round(taux, 3)
    return taux


def is_user_in_party():
    if not is_authenticated():
        return None
    user_id = session.get("user_id")
    try:
        with mysql.connection.cursor() as cur:
            return Party.get_id_for_user(cur, user_id)
    except Exception:
        return None


def get_consumption_by_party(party_id):
    if not is_authenticated():
        return jsonify({"success": False, "error": "Non authentifié"}), 401
    try:
        with mysql.connection.cursor() as cur:
            consumption = Consumption.get_consumption_by_party(cur, party_id)

            return jsonify({"success": True, "consumption": consumption})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500