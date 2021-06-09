from flask import Flask
from flask_cors import CORS
import os
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from dotenv import load_dotenv, find_dotenv
from routes.auth import auth_handler
from routes.api import api_handler


load_dotenv(find_dotenv())
JWT_SECRET = os.environ.get("JWT_SECRET")

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config["JWT_SECRET_KEY"] = JWT_SECRET
jwt = JWTManager(app)

app.register_blueprint(auth_handler, url_prefix="/auth")
app.register_blueprint(api_handler, url_prefix="/api")


if __name__ == '__main__':
    app.run(debug=True)
