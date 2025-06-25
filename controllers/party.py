from models.party import Party
from flask import jsonify, request, redirect, url_for, session, render_template
from db import mysql
from controllers.user import is_authenticated
from datetime import datetime
from controllers.utils import generate_qr_code

def create_party():
    if not is_authenticated():
        return redirect(url_for('login'))
    party_id = is_user_in_party()
    if party_id:
        return redirect(url_for('view_party_route', party_id=party_id))
    if request.method != "POST":
        return render_template("party/create.html")
    try:
        with mysql.connection.cursor() as cur:
            name = request.form.get("name")
            date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            id_organisateur = session.get("user_id")
            party_id, code = Party.create(cur, name, id_organisateur, date, status="ongoing")
            mysql.connection.commit()
        return redirect(url_for('view_party_route', party_id=party_id))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def view_party(party_id):
    if not is_authenticated():
        return redirect(url_for('login'))
    try:
        with mysql.connection.cursor() as cur:
            party = Party.get_by_id(cur, party_id)
            if not party:
                return redirect(url_for('create_party_route'))
            user_id = session.get("user_id")
            if party.id_organisateur != user_id and not Party.is_user_invited(cur, party_id, user_id):
                return jsonify({"error": "Unauthorized access"}), 403
            join_url = url_for('join_party_route', _external=True) + f"?code={party.code}"
            qr_code = generate_qr_code(join_url)
            user_drink_count = Party.count_user_drinks(cur, party_id, user_id)
            return render_template(
                "party/view.html",
                party=party,
                qr_code=qr_code,
                join_url=join_url,
                user_drink_count=user_drink_count
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_current_party():
    if not is_authenticated():
        return redirect(url_for('login'))
    user_id = session.get("user_id")
    try:
        with mysql.connection.cursor() as cur:
            party_id = Party.get_id_for_user(cur, user_id)
            if party_id:
                return redirect(url_for('view_party_route', party_id=party_id))
            return render_template("party/create.html", message="Pas de fête en cours.")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def is_user_in_party():
    if not is_authenticated():
        return None
    user_id = session.get("user_id")
    try:
        with mysql.connection.cursor() as cur:
            return Party.get_id_for_user(cur, user_id)
    except Exception:
        return None

def close_party(party_id):
    if not is_authenticated():
        return redirect(url_for('login'))
    try:
        with mysql.connection.cursor() as cur:
            party = Party.get_by_id(cur, party_id)
            if not party or party.id_organisateur != session.get("user_id"):
                return jsonify({"error": "Unauthorized access"}), 403
            if party.status == 'ongoing':
                Party.close(cur, party_id)
                mysql.connection.commit()
                return redirect(url_for("view_party_route", party_id=party_id))
            else:
                return jsonify({"error": "Party is already closed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def join_party():
    if not is_authenticated():
        return redirect(url_for('login'))
    code = request.args.get("code") or request.form.get("code")
    if code:
        try:
            with mysql.connection.cursor() as cur:
                party = Party.get_by_code(cur, code)
                if not party:
                    return render_template("party/join.html", error="Fête introuvable.")
                user_id = session.get("user_id")
                if not Party.is_user_invited(cur, party.id_soiree, user_id):
                    Party.add_invitation(cur, party.id_soiree, user_id)
                    mysql.connection.commit()
                return redirect(url_for('view_party_route', party_id=party.id_soiree))
        except Exception as e:
            return render_template("party/join.html", error=str(e))
    else:
        return render_template("party/join.html")

def leave_party():
    if not is_authenticated():
        return jsonify({"error": "Non authentifié"}), 401
    party_id = request.args.get("party_id") or request.form.get("code")
    if not party_id:
        return jsonify({"error": "ID de fête manquant"}), 400
    try:
        with mysql.connection.cursor() as cur:
            user_id = session.get("user_id")
            party = Party.get_by_id(cur, party_id)
            if not party:
                return jsonify({"error": "Fête introuvable"}), 404
            if Party.is_user_invited(cur, party_id, user_id):
                Party.remove_invitation(cur, party_id, user_id)
                mysql.connection.commit()
                return redirect(url_for('index'))
            else:
                return jsonify({"error": "Vous n'etes pas invité à cette fête."}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def party_stats(party_id):
    if not is_authenticated():
        return jsonify({"error": "Non authentifié"}), 401
    try:
        with mysql.connection.cursor() as cur:
            party = Party.get_by_id(cur, party_id)
            if not party:
                return jsonify({"error": "Fête introuvable"}), 404
            user_id = session.get("user_id")
            if party.id_organisateur != user_id and not Party.is_user_invited(cur, party_id, user_id):
                return jsonify({"error": "Accès non autorisé"}), 403
            stats = Party.get_party_stats(cur, party_id)
            return jsonify({"stats": stats})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def get_participants_for_party(party_id):
    if not is_authenticated():
        return jsonify({"error": "Non authentifié"}), 401
    try:
        with mysql.connection.cursor() as cur:
            party = Party.get_participants_in_party(cur, party_id)
            if not party:
                return jsonify({"error": "Fête introuvable"}), 404
            return jsonify({"participants": party})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
