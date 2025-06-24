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
    else:
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
            if party.id_organisateur != session.get("user_id"):
                if not cur.execute("""
                                   SELECT id_user
                                   FROM invitation
                                   WHERE id_soiree = %s
                                     AND id_user = %s
                                   """, (party_id, session.get("user_id"))):
                    return jsonify({"error": "Unauthorized access"}), 403
            if not party:
                return redirect(url_for('create_party_route'))
            join_url = url_for('join_party_route', _external=True) + f"?code={party.code}"
            qr_code = generate_qr_code(join_url)
            return render_template("party/view.html", party=party, qr_code=qr_code, join_url=join_url)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_current_party():
    if not is_authenticated():
        return redirect(url_for('login'))
    user_id = session.get("user_id")
    try:
        with mysql.connection.cursor() as cur:
            cur.execute("""
                        SELECT id_soiree
                        FROM soiree
                        WHERE (id_organisateur = %s OR id_soiree IN (SELECT id_soiree
                                                                     FROM invitation
                                                                     WHERE id_user = %s))
                          AND status = 'ongoing' LIMIT 1
                        """, (user_id, user_id))
            result = cur.fetchone()
            if result:
                party_id = result[0]
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
            cur.execute("""
                        SELECT id_soiree
                        FROM soiree
                        WHERE (id_organisateur = %s OR id_soiree IN (SELECT id_soiree
                                                                     FROM invitation
                                                                     WHERE id_user = %s))
                          AND status = 'ongoing' LIMIT 1
                        """, (user_id, user_id))
            result = cur.fetchone()
            if result:
                return result[0]
            return None
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
                cur.execute("UPDATE soiree SET status = 'finished' WHERE id_soiree = %s", (party_id,))
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
                # Vérifie si l'utilisateur est déjà invité
                cur.execute("SELECT 1 FROM invitation WHERE id_soiree = %s AND id_user = %s", (party.id_soiree, user_id))
                if not cur.fetchone():
                    cur.execute("INSERT INTO invitation (id_soiree, id_user) VALUES (%s, %s)", (party.id_soiree, user_id))
                    mysql.connection.commit()
                return redirect(url_for('view_party_route', party_id=party.id_soiree))
        except Exception as e:
            return render_template("party/join.html", error=str(e))
    else:
        return render_template("party/join.html")
