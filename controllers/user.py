from flask import request, jsonify, session, redirect, url_for, render_template
from models.user import User
from db import mysql
import uuid


def register():
    if request.method == "POST":
        nom = request.form.get("nom")
        prénom = request.form.get("prénom")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if password != confirm:
            return render_template("user/register.html", error="Les mots de passe ne correspondent pas")
        âge = request.form.get("âge")
        poids = request.form.get("poids")
        genre = request.form.get("genre")
        password = hash_password(password)
        session_token = uuid.uuid4().hex
        try:
            with mysql.connection.cursor() as cur:
                cur.execute(
                    "INSERT INTO utilisateur (nom, prénom, email, password, âge, poids, genre, session_token) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (nom, prénom, email, password, âge, poids, genre, session_token)
                )
                mysql.connection.commit()
                cur.execute("SELECT id_user FROM utilisateur WHERE email = %s", (email,))
                user_id = cur.fetchone()[0]
                session["user_id"] = user_id
                session["session_token"] = session_token
            return redirect(url_for('index'))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return render_template("user/register.html")


def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = hash_password(password)
        try:
            with mysql.connection.cursor() as cur:
                cur.execute("SELECT * FROM utilisateur WHERE email = %s", (email,))
                row = cur.fetchone()
                if row:
                    user = User(*row)
                    debug_data = user.__dict__.copy()
                    debug_data["hashed_password"] = hashed_password
                    return jsonify(debug_data)
                    if user.password == hashed_password:
                        session_token = uuid.uuid4().hex
                        cur.execute("UPDATE utilisateur SET session_token = %s WHERE id_user = %s",
                                    (session_token, user.id_user))
                        mysql.connection.commit()
                        session["user_id"] = user.id_user
                        session["session_token"] = session_token
                        return redirect(url_for('index'))
                    else:
                        return render_template("user/login.html", error="Mot de passe incorrect")
                else:
                    return render_template("user/login.html", error="Utilisateur non trouvé")
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return render_template("user/login.html")


def logout():
    session.pop("user_id", None)
    session.pop("session_token", None)
    return redirect(url_for('index'))


def hash_password(password):
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()


def is_authenticated():
    user_id = session.get("user_id")
    session_token = session.get("session_token")
    if not user_id or not session_token:
        return False
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT session_token FROM utilisateur WHERE id_user = %s", (user_id,))
        row = cur.fetchone()
        if row and row[0] == session_token:
            return True
    return False


def get_user_by_id(user_id):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM utilisateur WHERE id_user = %s", (user_id,))
        row = cur.fetchone()
        if row:
            return User(*row)
    return None


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return get_user_by_id(user_id)


def profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for('login'))
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM utilisateur WHERE id_user = %s", (user_id,))
        row = cur.fetchone()
        if row:
            user = User(*row)
            return render_template("user/profile.html", user=user)
    return redirect(url_for('login'))
