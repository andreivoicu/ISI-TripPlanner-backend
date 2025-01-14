import os
import requests
from flask import request, jsonify # type: ignore
from . import app
from .services.auth_service import *
from .services.user_service import *
from .services.route_service import *
from .services.poi_service import *

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

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
    print(data)
    if not data:
        return jsonify({'error': 'Missing data'}), 400
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return jsonify({'error': 'Invalid Authorization header format'}), 400   
    token = token.split(' ')[1]
    print(token)
    if token:     
        return update_user(data, token)
    else:
        return jsonify({"error": "Username not provided"}), 400

@app.route('/places/google', methods=['GET'])
def get_place_suggestions_google():
    print("entered endpoint function")
    print(f"API key: {GOOGLE_API_KEY}")

    params = {
        "location": request.args.get('location'),
        "radius": request.args.get('radius'),
        "keyword": request.args.get('keyword'),
        "key": GOOGLE_API_KEY,
    }

    print(params)

    response = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=params)

    return jsonify(response.json())

@app.route('/routes', methods=['POST'])
def create_route():

    token = request.headers.get('Authorization')

    if not token or not token.startswith('Bearer '):
        return jsonify({'error': 'Invalid Authorization header format'}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing data'}), 400
    token = token.split(' ')[1]
    return add_route(data, token)
    
@app.route('/routes', methods=['GET'])
def get_routes():
    token = request.headers.get('Authorization')

    if not token or not token.startswith('Bearer '):
        return jsonify({'error': 'Invalid Authorization header format'}), 400
    
    token = token.split(' ')[1]
    return get_routes_by_token(token)

@app.route('/places', methods=['GET'])
def get_places():
    return get_pois()

    
