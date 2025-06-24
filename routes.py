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

# Routes pour les utilisateurs
@app.route("/register", methods=["GET", "POST"])
def register_route():
    if "user_id" in session:
        return redirect("/")
    if request.method == "POST":
        return register()
    else:
        return render_template("user/register.html")


@app.route("/login", methods=["GET", "POST"])
def login_route():
    if "user_id" in session:
        return redirect("/")
    if request.method == "POST":
        return login()
    else:
        return render_template("user/login.html")


@app.route("/logout")
def logout_route():
    return logout()

@app.route("/profile")
def profile_route():
    if "user_id" not in session:
        return redirect("/login")
    return profile()