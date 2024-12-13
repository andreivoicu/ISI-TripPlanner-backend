from flask import jsonify # type: ignore
from .validators import validate_user_data
from ..utils import hash_password
from ..db_queries import add_user, get_user_by_username, verify_if_user_exists
from ..utils import generate_token, check_password

def register_user(data):
    validation_result = validate_user_data(data)
    if validation_result is not True:
        return jsonify({'error': validation_result}), 400

    hashed_password = hash_password(data['password'])

    response, response_code = verify_if_user_exists(data['username'], data['email'])
    if response:
        return jsonify({'error': response}), response_code

    return add_user(
        first_name=data['first_name'],
        last_name=data['last_name'],
        username=data['username'],
        password=hashed_password,
        email=data['email']
    )

def login_user(data):
    username = data.get('username')
    password = data.get('password')

    user = get_user_by_username(username)
    if not user:
        return jsonify({'error': 'Invalid username'}), 400

    if check_password(password, user.password):
        token = generate_token(user)
        return jsonify({'message': 'Login successful', 'token': token}), 200

    return jsonify({'error': 'Invalid credentials'}), 401
