from app_instance import app
from controllers.drink import *
from controllers.user import *
from controllers.party import *
from controllers.consumption import *
from controllers.utils import index_t

@app.route('/')
def index():
    return index_t()

@app.route("/drinks")
def drinks():
    return get_all_drinks()


# Routes pour les boissons
@app.route("/drinks/create", methods=["POST"])
def create_drink_route():
    return create_drink();


@app.route("/drinks/create", methods=["GET"])
def add_drink():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("drinks/add.html");


@app.route('/drinks/<int:drink_id>')
def single_drink_route(drink_id):
    return single_drink(drink_id)

@app.route('/drinks/search')
def search_drinks_route():
    return search_drinks()

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

@app.route("/profile/edit", methods=["POST"])
def edit_profile_route():
    if "user_id" not in session:
        return redirect("/login")
    else:
        return edit_profile()


# Routes pour les soirées
@app.route("/create_party", methods=["GET", "POST"])
def create_party_route():
    if "user_id" not in session:
        return redirect("/login")
    else:
        return create_party()

@app.route("/party/<int:party_id>")
def view_party_route(party_id):
    if "user_id" not in session:
        return redirect("/login")
    return view_party(party_id)

@app.route("/current_party")
def current_party_route():
    if "user_id" not in session:
        return redirect("/login")
    return get_current_party()

@app.route('/close_party/<int:party_id>', methods=['POST'])
def close_party_route(party_id):
    return close_party(party_id)

@app.route('/party/join', methods=['POST', 'GET'])
def join_party_route():
    if "user_id" not in session:
        return redirect("/login")
    else:
        return join_party()

@app.route('/party/add_conso', methods=['POST', 'GET'])
def add_conso_route():
    if "user_id" not in session:
        return redirect("/login")
    else:
        return add_conso()

@app.route('/party/write_taux', methods=['GET'])
def write_taux_route():
    if "user_id" not in session:
        return jsonify({"taux": 0})

    taux = calculer_taux_alcoolemie(session["user_id"])
    return jsonify({"taux": taux})


@app.route('/party/<int:party_id>/stats', methods=['GET'])
def party_stats_route(party_id):
    return party_stats(party_id)

@app.route('/stats')
def stats_route():
    if "user_id" not in session:
        return redirect("/login")
    return stats()

@app.route('/api/participants/<int:party_id>')
def get_participants(party_id):
    return get_participants_for_party(party_id)


@app.route('/party/<int:party_id>/history')
def party_history_route(party_id):
    return get_consumption_by_party(party_id)