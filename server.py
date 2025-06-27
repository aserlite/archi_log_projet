from app_instance import app
from flask_cors import CORS
import routes
import os
from dotenv import load_dotenv

load_dotenv()

CORS(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config["SERVER_NAME"] = "192.168.0.15:5000"
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB
app.config['MAX_FORM_MEMORY_SIZE'] = 50 * 1024 * 1024  # 50 MB



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
