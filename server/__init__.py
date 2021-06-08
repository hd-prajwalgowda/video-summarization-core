from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
import os
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
BACKEND_URL = os.environ.get("BACKEND_URL")
JWT_SECRET = os.environ.get("JWT_SECRET")

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config["JWT_SECRET_KEY"] = JWT_SECRET
jwt = JWTManager(app)

client = MongoClient(BACKEND_URL)
db = client['videosum']
users = db['users']

from server import routes
