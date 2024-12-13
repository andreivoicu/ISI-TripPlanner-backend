from ..db_queries import add_route
from flask import jsonify # type: ignore
from ..db_queries import get_users

def add_route_to_user(data):
    required_fields = ['city', 'total_time_spent', 'user_id']
    if not all([field in data for field in required_fields]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # verify if user_id exists
    users = get_users()
    user_ids = [user.id for user in users]
    if data['user_id'] not in user_ids:
        return jsonify({'error': 'User does not exist'}), 400
    user = users[user_ids.index(data['user_id'])]
    return add_route(
        city=data['city'],
        total_time_spent=data['total_time_spent'],
        user_id=user.id
    )