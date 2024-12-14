from flask import jsonify # type: ignore
from ..db_queries import *
from .validators import *

def get_all_users():
    users = get_users()
    return jsonify([user.serialize() for user in users])

def get_user_by_username(username):
    
    if username == '' :
        return jsonify({'error': 'Username not provided'}), 400
    user = get_user_from_db_by_username(username)
    if user:
        return jsonify(user.serialize()), 200
    return jsonify({'error': 'User not found'}), 404

def get_user_by_id(id):
    
    user = get_user_from_db_by_id(id)
    if user:
        return jsonify(user.serialize()), 200
    return jsonify({'error': 'User not found'}), 404

def delete_user_by_username(username):

    if username == '' :
        return jsonify({'error': 'Username not provided'}), 400
    return delete_user_from_db(username)

def update_user(data):

    if 'id' not in data:
        return jsonify({'error': 'No user id provided'}), 400
    
   
    fields_to_update = ['username', 'email', 'password', 'first_name', 'last_name']

    if not any(field in data for field in fields_to_update):
        return jsonify({'error': 'No valid data provided'}), 400

    for field in fields_to_update:
        if field in data:
            if field == 'username':
                validation_result = validate_username(data[field])
            elif field == 'password':
                validation_result = validate_password(data[field])
            elif field == 'email':
                validation_result = validate_email(data[field])
            elif field == 'first_name' or field == 'last_name':
                validation_result = validate_name(data[field], field)
        
            if validation_result is not True:
                return validation_result, 400
            
            result = update_user_in_db(field, data[field], data['id'])
            if result[1] != 200:
                return result
    
    return jsonify({'message': 'User updated successfully'}), 200
