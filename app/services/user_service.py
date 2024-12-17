from flask import jsonify # type: ignore
from ..db_queries import *
from .validators import *
from ..utils import decode_token

def get_all_users():
    users = get_users()
    return jsonify([user.serialize() for user in users])

def get_user_by_token(token):
    if token == '' :
        return jsonify({'error': 'Token not provided'}), 400
    payload = decode_token(token)
    if payload:
        user_id = int(payload['user_id'])
        user = get_user_from_db_by_id(user_id)
        if user:
            return jsonify(user.serialize()), 200
    return jsonify({'error': 'User not found'}), 404

def delete_user_by_token(token):
    if token == '' :
        return jsonify({'error': 'Token not provided'}), 400
    payload = decode_token(token)
    if payload:
        user_id = int(payload['user_id'])
        return delete_user_from_db(user_id)
    return jsonify({'error': 'User not found'}), 404
   
    

def update_user(data, token):

    if token == '' :
        return jsonify({'error': 'Token not provided'}), 400
   
    fields_to_update = ['username', 'email', 'password', 'first_name', 'last_name']

    if not any(field in data for field in fields_to_update):
        return jsonify({'error': 'No valid data provided'}), 400
    
    payload = decode_token(token)
    if payload:
        user_id = int(payload['user_id'])

    user = get_user_from_db_by_id(user_id)
    user = user.serialize()

    for field in fields_to_update:
        if field in data and data[field] != user[field]:      
            if field == 'username':
                validation_result = validate_username(data[field])
            elif field == 'password':
                validation_result = validate_password(data[field])
            elif field == 'email':
                validation_result = validate_email(data[field])
            elif field == 'first_name' or field == 'last_name':
                validation_result = validate_name(data[field], field)
        
            if validation_result is not True:
                return jsonify({'error': validation_result}), 400
            
            result = update_user_in_db(field, data[field], user_id)
            if result[1] != 200:
                return jsonify({'error': result[0]}), 400
    
    return jsonify({'message': 'User updated successfully'}), 200
