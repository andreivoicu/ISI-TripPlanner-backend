from flask import Flask
from flask import request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import re
import bcrypt

app = Flask(__name__)

DATABASE_URL = "postgresql://postgres:admin@localhost:5432/ISIroute"

# Initialize SQLAlchemy
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    email = Column(String(100), unique=True, nullable=False)

# Function to create the tables (in case they don't exist yet)
def create_tables():
    Base.metadata.create_all(bind=engine)

# Function to add a user
def add_user(first_name: str, last_name: str, username: str, password: str, email: str):
    db = SessionLocal()
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
        password=password,
        email=email
    )
    try:
        db.add(new_user)  # Add the user object to the session
        db.commit()  # Commit the transaction to the database
        db.refresh(new_user)  # Refresh the instance to get the new ID from the database
        return f"User {new_user.username} added successfully!", 201
    except Exception as e:
        db.rollback()  # In case of error, rollback the transaction
        return f"Error adding user: {e}", 500
    finally:
        db.close()  # Always close the session

def get_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users

def validate_username(username):
    if not username or len(username) < 3 or len(username) > 20:
        return "Username must be between 3 and 20 characters."
    if not re.match(r'^\w+$', username):
        return "Username must contain only alphanumeric characters and underscores."
    return True

def validate_password(password):
    if not password or len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r'[A-Za-z]', password):
        return "Password must include at least one letter."
    if not re.search(r'\d', password):
        return "Password must include at least one number."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "Password must include at least one special character."
    return True

def validate_email(email):
    if not email or not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        return "Invalid email format."
    return True

def validate_name(name, field_name):
    if not name or not re.match(r'^[A-Za-z\s\-]{1,50}$', name):
        return f"{field_name} must be 1-50 characters long and contain only letters, spaces, and hyphens (-)."
    return True

def hash_password(password):
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed

def check_password(password, hashed):
    password_bytes = password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed)


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Missing data'}), 400
        
        required_fields = ['firstName', 'lastName', 'username', 'password', 'email']
        missing_field = next((field for field in required_fields if field not in data), None)
        if missing_field:
            return jsonify({'error': f'Missing {missing_field}'}), 400

        [firstName, lastName, username, password, email] = [data.get(field) for field in required_fields]

        fields = [
            (firstName, lambda value: validate_name(value, 'First name')),
            (lastName, lambda value: validate_name(value, 'Last name')),
            (username, validate_username),
            (password, validate_password),
            (email, validate_email),
        ]

        for value, validator in fields:
            if (is_valid := validator(value)) is not True:
                return jsonify({'error': is_valid}), 400
                
        hashed_password = hash_password(password)
        response_message, response_code = add_user(first_name=firstName, last_name=lastName, username=username, password=hashed_password, email=email)
        
        # users = get_users()
        # print(users)

        return jsonify({'message': response_message}), response_code


if __name__ == '__main__':
    app.run()
    create_tables()