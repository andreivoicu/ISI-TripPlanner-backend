from flask import request, jsonify # type: ignore
from . import app
from .services.auth_service import register_user, login_user
from .services.user_service import get_all_users

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

@app.route('/user', methods=['GET'])
def get_users():
    return get_all_users()