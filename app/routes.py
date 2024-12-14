from flask import request, jsonify # type: ignore
from . import app
from .services.auth_service import *
from .services.user_service import *
from .services.route_service import *


@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Missing data'}), 400
    
    return register_user(data)

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Missing data'}), 400
    
    return login_user(data)

@app.route('/users', methods=['GET'])
def get_users():
    return get_all_users()

@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username')
    if username:
        return get_user_by_username(username)
    else:
        return jsonify({"error": "Username not provided"}), 400

@app.route('/user', methods=['DELETE'])
def delete_user():
    username = request.args.get('username')
    if username:
        return delete_user_by_username(username)
    else:
        return jsonify({"error": "Username not provided"}), 400
    
@app.route('/user', methods=['PUT'])
def update_user_by_id():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing data'}), 400
    return update_user(data)

    
