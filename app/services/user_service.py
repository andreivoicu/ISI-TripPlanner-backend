from flask import jsonify # type: ignore
from ..db_queries import get_users

def get_all_users():
    users = get_users()
    return jsonify([user.serialize() for user in users])