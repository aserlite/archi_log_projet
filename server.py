from app_instance import app
from flask_cors import CORS
import routes
import os
from dotenv import load_dotenv

load_dotenv()

CORS(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config["SERVER_NAME"] = "192.168.193.194:5000"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
