from flask import request, jsonify, session, redirect, url_for
from db import mysql
from controllers.user import is_authenticated
from models.consumption import Consumption
from models.party import Party
from models.user import User
from models.drink import Drink
from datetime import datetime, timedelta


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


def calculer_taux_alcoolemie(user_id, party_id=None):
    instant_T = datetime.now()
    dose_alcool = 10
    elimination = 0.15

    cursor = mysql.connection.cursor()
    user = User.get_by_id(cursor, user_id)
    if not user:
        return {"taux": 0, "heure_reprise": None}

    poids = user.poids
    genre = user.genre
    coef = 0.7 if genre == 'Homme' else 0.6

    if not party_id:
        party_id = Party.get_id_for_user(cursor, user_id)
    if not party_id:
        return {"taux": 0, "heure_reprise": None}

    consommations = Consumption.get_consumption_by_user_by_party(cursor, user_id, party_id)
    alcool_total = 0
    for conso in consommations:
        if not Drink.is_alcoholic(cursor, conso.id_boisson):
            continue
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

    heure_reprise = None

    if taux >= 0.5:
        for h in range(1, 25):
            alcool_total_h = 0
            for conso in consommations:
                if not Drink.is_alcoholic(cursor, conso.id_boisson):
                    continue
                if isinstance(conso.timestamp, str):
                    conso_time = datetime.fromisoformat(conso.timestamp)
                else:
                    conso_time = conso.timestamp
                heures_ecoulees = (instant_T + timedelta(hours=h) - conso_time).total_seconds() / 3600
                if heures_ecoulees < 0:
                    continue
                alcool_restant = dose_alcool * conso.quantité - elimination * heures_ecoulees
                if alcool_restant > 0:
                    alcool_total_h += alcool_restant
            taux_h = alcool_total_h / (float(poids) * float(coef)) if poids and coef else 0
            if taux_h > 0.5:
                heure_reprise_dt = (instant_T + timedelta(hours=h)).replace(second=0, microsecond=0)
                heure_reprise = heure_reprise_dt.strftime("%H:%M")
                if heure_reprise_dt.date() > instant_T.date():
                    heure_reprise = f"demain à {heure_reprise}"
                break

    return {"taux": taux, "heure_reprise": heure_reprise}

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