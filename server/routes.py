from server import app, users
from flask import request, jsonify
import json
import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@app.route('/name', methods=['GET'])
@jwt_required()
def get_all_users():
  current_user_id = get_jwt_identity()
  names = users.find({'email': current_user_id},{'name': 1, "_id": 0, 'email': 1})
  arr = list(names)
  for x in names:
    print(x)
  print(arr)
  return json.dumps({'names':arr})

@app.route('/signup', methods=['POST'])
def user_sign_up():
  request_data = request.get_json()
  user_name = request_data['name']
  user_email = request_data['email']
  user_password = request_data['password']
  email_found = users.find_one({"email": user_email})
  if email_found:
    message = 'There already is a user by that email'
    return jsonify({'success': False, 'err': message}), 202
  pw_hash = bcrypt.hashpw(user_password.encode('utf8'), bcrypt.gensalt())
  user_input = {'name': user_name, 'email': user_email, 'password': pw_hash}
  userInsert = users.insert_one(user_input)
  # print(userInsert.inserted_id)
  access_token = create_access_token(identity=user_email)
  return jsonify({'login': True, 'msg': 'User created', 'success': True, 'token': access_token}), 200

@app.route('/login', methods=['POST'])
def user_login():
  try:
    request_data = request.get_json()
    user_email = request_data['email']
    user_password = request_data['password']
    user_data = users.find_one({"email": user_email})
    try:
      user_data
      passwd = bcrypt.checkpw(user_password.encode('utf8'), user_data['password'])
      if (passwd):
        access_token = create_access_token(identity=user_email)
        return jsonify({'login': True, 'msg':'user logged in', 'success': True, 'token': access_token}), 200
      else:
        return jsonify({'login': False, 'msg':'user password incorrect'}), 403
    except:
      return jsonify({'err': 'User data not found'}), 401
  except:
    return jsonify({'err': 'Internal server error'}), 500