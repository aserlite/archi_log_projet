from flask import request, jsonify, session, redirect, url_for, render_template
from models.user import User
from db import mysql
import uuid


def register():
    if request.method == "POST":
        pseudo = request.form.get("pseudo")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if len(password) < 8:
            return render_template("user/register.html", error="Le mot de passe doit contenir au moins 8 caractères")
        if password != confirm:
            return render_template("user/register.html", error="Les mots de passe ne correspondent pas")
        age = request.form.get("âge")
        age = int(age)
        if (age < 18):
            return redirect('https://www.youtubekids.com/')
        poids = request.form.get("poids")
        genre = request.form.get("genre")
        password = hash_password(password)
        session_token = uuid.uuid4().hex
        try:
            with mysql.connection.cursor() as cur:
                User.create(cur, pseudo, email, password, age, poids, genre, session_token)
                mysql.connection.commit()
                user_id = User.get_id_by_email(cur, email)
                session["user_id"] = user_id
                session["session_token"] = session_token
            code = request.args.get("code")
            if code:
                return redirect(url_for('join_party_route', code=code))
            else:
                return redirect(url_for('index'))
        except Exception as e:
            if(e.args[0] == 1062):
                return render_template("user/register.html", error="L'email est déjà utilisé")
            return jsonify({"error": str(e)}), 500
    return render_template("user/register.html")


def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = hash_password(password)
        try:
            with mysql.connection.cursor() as cur:
                user = User.get_by_email(cur, email)
                if user:
                    if user.password == hashed_password:
                        session_token = uuid.uuid4().hex
                        User.update_session_token(cur, user.id_user, session_token)
                        mysql.connection.commit()
                        session["user_id"] = user.id_user
                        session["session_token"] = session_token
                        code = request.args.get("code")
                        if code:
                            return redirect(url_for('jo in_party_route', code=code))

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
        token = User.get_session_token(cur, user_id)
        if token and token == session_token:
            return True
    return False


def get_user_by_id(user_id):
    with mysql.connection.cursor() as cur:
        return User.get_by_id(cur, user_id)


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
        user = User.get_by_id(cur, user_id)
        if user:
            return render_template("user/profile.html", user=user)
    return redirect(url_for('login'))

def edit_profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for('login'))
    if request.method == "POST":
        pseudo = request.form.get("pseudo")
        email = request.form.get("email")
        âge = request.form.get("âge")
        poids = request.form.get("poids")
        genre = request.form.get("genre")
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        with mysql.connection.cursor() as cur:
            user = User.get_by_id(cur, user_id)
            if not user or user.password != hash_password(current_password):
                return render_template("user/profile.html", user=user, error="Mot de passe actuel incorrect.")
            if new_password:
                password = hash_password(new_password)
            else:
                password = user.password
            try:
                User.update_profile(cur, user_id, pseudo, email, âge, poids, genre, password)
                mysql.connection.commit()
                return render_template("user/profile.html", user=User.get_by_id(cur, user_id), success="Profil mis à jour avec succès.")
            except Exception as e:
                return render_template("user/profile.html", user=user, error="Erreur lors de la mise à jour du profil.")
    else:
        with mysql.connection.cursor() as cur:
            user = User.get_by_id(cur, user_id)
        return render_template("user/profile.html", user=user)

def stats():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for('login'))
    with mysql.connection.cursor() as cur:
        user = User.get_by_id(cur, user_id)
        stats = User.get_stats(cur, user_id)
        parties = User.get_parties_with_counts(cur, user_id)
    return render_template("user/stats.html", user=user, stats=stats, parties=parties)