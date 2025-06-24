from app_instance import app
from controllers.drink import *
from controllers.user import *


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/drinks")
def drinks():
    return get_all_drinks()


# Routes pour les boissons
@app.route("/drinks/create", methods=["POST"])
def create_drink_route():
    return create_drink();


@app.route("/drinks/create", methods=["GET"])
def add_drink():
    return render_template("drinks/add.html");


@app.route('/drinks/<int:drink_id>')
def single_drink_route(drink_id):
    return single_drink(drink_id)