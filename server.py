from flask import Flask, request, render_template, jsonify, redirect
from flask_cors import CORS
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)