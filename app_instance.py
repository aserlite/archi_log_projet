from flask import Flask
app = Flask(__name__)

@app.context_processor
def inject_user():
    from controllers.user import get_current_user
    return {'user': get_current_user()}