import random
import qrcode
import io
import base64
import os
from flask import render_template, session, jsonify
from controllers.user import is_authenticated
from db import mysql
from models.party import Party
from controllers.consumption import calculer_taux_alcoolemie

def generate_qr_code(data):
    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return img_b64

def index_t():
    citations_dir = os.path.join('static', 'images', 'citations')
    fichiers = [f for f in os.listdir(citations_dir) if os.path.isfile(os.path.join(citations_dir, f))]
    citation_img = None
    if fichiers:
        citation_img = os.path.join('images', 'citations', random.choice(fichiers))
    current_party = None
    if 'user_id' in session:
        party_id = is_user_in_party()
        user_id = session.get("user_id")
        if party_id:
            cur = mysql.connection.cursor()
            user_drink_count = Party.count_user_drinks(cur, party_id, user_id)
            alcoolemie = calculer_taux_alcoolemie(session.get("user_id"))
            current_party = {
                'party_id': party_id,
                'user_drink_count': user_drink_count,
                'alcoolemie': alcoolemie
            }
            cur.close()
    return render_template('index.html', citation_img=citation_img, current_party=current_party)


def is_user_in_party():
    if not is_authenticated():
        return None
    user_id = session.get("user_id")
    try:
        with mysql.connection.cursor() as cur:
            return Party.get_id_for_user(cur, user_id)
    except Exception:
        return None