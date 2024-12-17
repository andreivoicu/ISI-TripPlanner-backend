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
    # get token from header 
    token = request.headers.get('Authorization')

    if not token or not token.startswith('Bearer '):
        return jsonify({'error': 'Invalid Authorization header format'}), 400
    
    token = token.split(' ')[1]
    if token:
        return get_user_by_token(token)
    else:
        return jsonify({"error": "Token not provided"}), 400

@app.route('/user', methods=['DELETE'])
def delete_user():

    token = request.headers.get('Authorization')

    if not token or not token.startswith('Bearer '):
        return jsonify({'error': 'Invalid Authorization header format'}), 400
    
    token = token.split(' ')[1]
    if token:
        
        return delete_user_by_token(token)
    else:
        return jsonify({"error": "Username not provided"}), 400
    
@app.route('/user', methods=['PUT'])
def update_user_by_token():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing data'}), 400
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return jsonify({'error': 'Invalid Authorization header format'}), 400   
    token = token.split(' ')[1]
    if token:     
        return update_user(data, token)
    else:
        return jsonify({"error": "Username not provided"}), 400

    
