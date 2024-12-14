from flask import jsonify # type: ignore
from . import SessionLocal
from .models import User

def add_user(first_name, last_name, username, password, email):
    db = SessionLocal()
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
        password=password,
        email=email
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

def get_user_from_db_by_username(username):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user

def get_user_from_db_by_id(id):
    db = SessionLocal()
    user = db.query(User).filter(User.id == id).first()
    db.close()
    return user

def verify_if_user_exists(username, email):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if user:
        return 'Username already exists', 400
    user = db.query(User).filter(User.email == email).first()
    if user:
        return 'Email already exists', 400
    return None, 200

def delete_user_from_db(username):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if user:
        db.delete(user)
        db.commit()
        return jsonify({'message': f"User {username} deleted successfully"}), 200
    return jsonify({'error': 'User not found'}), 404

def update_user_in_db(field, value, id):

    if field == 'username' and verify_if_user_exists(value, '') != (None, 200):
        return jsonify({'error': 'Username already exists'}), 400
    if field == 'email' and verify_if_user_exists('', value) != (None, 200):
        return jsonify({'error': 'Email already exists'}), 400

    
    db = SessionLocal()
    user = db.query(User).filter(User.id == id).first()
    if user:
        setattr(user, field, value)
        db.commit()
        return jsonify({'message': f"User {user.username} updated successfully with {value} on {field}"}), 200
    return jsonify({'error': 'User not found'}), 404

