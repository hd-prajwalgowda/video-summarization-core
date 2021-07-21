import json
import os
from pymongo import MongoClient
from flask import Flask, request, Response, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from modules.db import DB
from utils.converter import convert_time_to_frame, convert_frames_to_summary


db = DB()
users = db.get_user_collection()


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
# @jwt_required()
def upload_summary():
    try:
        request_data = request.get_json()
        # "00:10,00:13\n00:21,00:26\n..."
        time_stamps = request_data['timeStamp']
        user = request_data['user']
        video = request_data['video']
        print(time_stamps, user, video)
        f_sections = convert_time_to_frame(time_stamps, 24)
        frames = convert_frames_to_summary(f_sections, 24)
        print(f_sections,frames)
        return Response(json.dumps({'login': True, 'msg': 'User Logged in', 'success': True, 'sum': 'generated'})), 200

    except:
        return 0


@api_handler.route('/get_videos', methods=['GET'])
@jwt_required()
def get_videos():
    videos = []
    return Response(json.dumps({"videos": videos}))

@api_handler.route('/upload_video', methods=['POST'])
# @jwt_required()
def upload_video():
    try:
        # request_data = request.get_json()
        print(request.files.getlist("file"))
        base64_file = request.files['file']
        base64_file.save(os.path.join("videos",base64_file.filename))
        return Response(json.dumps({'video': 'uploaded'}))

    except Exception as e:
        print("this is  exception...." ,e)
        return 0
