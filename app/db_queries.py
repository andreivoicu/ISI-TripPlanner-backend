from flask import jsonify # type: ignore
from . import SessionLocal
from .models import User, Route

def add_user(first_name, last_name, username, password, email):
    db = SessionLocal()
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
        password_hash=password,
        email_address=email
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return jsonify({'message': f"User {new_user.username} added successfully!"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': f"Error adding user: {e}"}), 500
    finally:
        db.close()

def get_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return users
    finally:
        db.close()

def get_user_by_username(username):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user

def verify_if_user_exists(username, email):
    users = get_users()
    for user in users:
        if username == user.username:
            return 'Username already exists', 400
        elif email == user.email:
            return 'Email already exists', 400
    return False, 200

def add_route(city, total_time_spent, user_id):
    db = SessionLocal()
    new_route = Route(
        city=city,
        total_time_spent=total_time_spent,
        user_id=user_id,
        route=0
    )
    try:
        db.add(new_route)
        db.commit()
        db.refresh(new_route)
        return jsonify({'message': f"Route added successfully!"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': f"Error adding route: {e}"}), 500
    finally:
        db.close()
