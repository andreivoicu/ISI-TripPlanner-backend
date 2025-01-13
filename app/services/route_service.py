from ..db_queries import add_route
from flask import jsonify # type: ignore
from ..db_queries import *
from ..utils import decode_token

def add_route(data, token):
    if token == '' :
        return jsonify({'error': 'Token not provided'}), 400
    if token == '' :
        return jsonify({'error': 'Token not provided'}), 400
    payload = decode_token(token)    
    if payload:
        user_id = int(payload['user_id'])
        return add_route_to_db(data['city'], data['sites'], user_id)
    return jsonify({'error': 'User not found'}), 404

def get_routes_by_token(token):
    if token == '' :
        return jsonify({'error': 'Token not provided'}), 400
    payload = decode_token(token)    
    if payload:
        user_id = int(payload['user_id'])
        routes = get_routes_by_user_id(user_id)
        return jsonify([route.serialize() for route in routes])
    return jsonify({'error': 'User not found'}), 404