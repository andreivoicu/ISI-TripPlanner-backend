from flask import jsonify # type: ignore
from . import SessionLocal
from .models import User, Route, PointOfInterest
import datetime
from sqlalchemy.orm import joinedload


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

def add_route_to_db(city, total_time_spent, user_id):
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
        
def verify_if_user_exists(username, email):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if user:
        print('Username already exists')
        return 'Username already exists', 400
    user = db.query(User).filter(User.email == email).first()
    if user:
        return 'Email already exists', 400
    return None, 200

def delete_user_from_db(id):
    db = SessionLocal()
    user = db.query(User).filter(User.id == id).first()
    if user:
        db.delete(user)
        db.commit()
        return jsonify({'message': f"User {user.username} deleted successfully"}), 200
    return jsonify({'error': 'User not found'}), 404

def update_user_in_db(field, value, id):
    print('Entering update_user_in_db')
    if field == 'username' and verify_if_user_exists(value, '') != (None, 200):
        return 'Username already exists', 400
    if field == 'email' and verify_if_user_exists('', value) != (None, 200):
        return 'Email already exists', 400
    print('Updating user')
    
    db = SessionLocal()
    user = db.query(User).filter(User.id == id).first()
    if user:
        setattr(user, field, value)
        db.commit()
        return jsonify({'message': f"User {user.username} updated successfully with {value} on {field}"}), 200
    return jsonify({'error': 'User not found'}), 404


def add_point_of_interest_to_db(name, latitude, longitude, route_id, rating, db):

    # db = SessionLocal()
    new_point_of_interest = PointOfInterest(
        name=name,
        latitude=latitude,
        longitude=longitude,
        route_id=route_id,
        rating=rating
    )
    try:
        db.add(new_point_of_interest)
        db.commit()
        db.refresh(new_point_of_interest)
        print("point of interest added successfully!")
        return jsonify({'message': f"Point of interest {name} added successfully!"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': f"Error adding point of interest {name}: {e}"}), 500
    
def search_points_of_interest_by_route_id(route_id, db):
    points = db.query(PointOfInterest).options(joinedload(PointOfInterest.route)).filter(PointOfInterest.route_id == route_id).all()
    print(points)
    return points

def get_points_of_interest():
    db = SessionLocal()
    points = db.query(PointOfInterest).all()
    db.close()
    return points


def add_route_to_db(city, points_list, user_id):
    timestamp = datetime.datetime.now()
    new_route = Route(
        city=city,
        user_id=user_id,
        timeSTAMP = timestamp
    )

    db = SessionLocal()
    try:
        db.add(new_route)
        db.commit()
        db.refresh(new_route)
        print("Route added successfully!")
    except Exception as e:
        db.rollback()
        print("Error adding route: {e}")
    
    print(new_route.id)

    for point in points_list:
        print(point)
        print(type(point))
        add_point_of_interest_to_db(point['name'], point['latitude'], point['longitude'], new_route.id, point['rating'], db)

    db = SessionLocal()
    new_route = db.query(Route).filter_by(id=new_route.id).first()
    #put the points in route
    new_route.points_of_interest = search_points_of_interest_by_route_id(new_route.id, db)
    db.commit()
    db.close()
    return jsonify({'message': f"Route added successfully!"}), 201

def get_routes_by_user_id(user_id):
    db = SessionLocal()
    routes = db.query(Route).options(joinedload(Route.points_of_interest)).filter(Route.user_id == user_id).all()

    db.close()
    return routes


    
