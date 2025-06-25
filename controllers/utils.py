import random
import qrcode
import io
import base64
import os
from flask import render_template

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
    return render_template('index.html', citation_img=citation_img)