from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask,request,Response,Blueprint
from flask import Flask,request,Response,Blueprint
from pymongo import MongoClient
import os
import json

BACKEND_URL = os.environ.get("BACKEND_URL")
client = MongoClient(BACKEND_URL)
db = client['videosum']
users = db['users']

api_handler = Blueprint('api', __name__)


@api_handler.route('/name', methods=['GET'])
@jwt_required()
def get_all_users():
    current_user_id = get_jwt_identity()
    names = users.find({'email': current_user_id}, {
                       'name': 1, "_id": 0, 'email': 1})
    arr = list(names)
    for x in names:
        print(x)
    print(arr)
    return json.dumps({'names': arr})

@api_handler.route('/upload_summary', methods=['POST'])
@jwt_required()
def upload_summary():
    try:
        request_data = request.get_json()
        # "00:10,00:13\n00:21,00:26\n..."
        time_stamps = request_data['time_stamps']
        return 0
    except:
        return 0

@api_handler.route('/get_videos', methods=['GET'])
@jwt_required()
def get_videos():
    videos = []
    return Response(json.dumps({"videos": videos}))
