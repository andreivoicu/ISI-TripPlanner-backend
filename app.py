from flask import Flask
from flask import request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import re
import bcrypt
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ISIproiect2024'
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
        return jsonify({'message': f"User {new_user.username} added successfully!"}), 201
    except Exception as e:
        db.rollback()  # In case of error, rollback the transaction
        return jsonify({'error': f"Error adding user: {e}"}), 500
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
    hashed = hashed.decode('utf-8')
    return hashed

def check_password(password, hashed):
    password_bytes = password.encode('utf-8')
    hashed = hashed.encode('utf-8')
    print(password_bytes)
    print(hashed)
    return bcrypt.checkpw(password_bytes, hashed)

def verify_if_user_exists(username, email):
    users = get_users()
    for user in users:
        if username == user.username:
            return 'Username already exists', 400
        elif email == user.email:
            return 'Email already exists', 400
    return False, 200

def generate_token(user):
    # Create a dictionary payload to encode in the JWT
    payload = {
        'sub': user.id,  # Subject, user ID
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expiration time (1 hour)
    }
    # Encode the payload with the secret key
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")
    return token


@app.route('/auth/register', methods=['POST'])
def register():
    create_tables()
    if request.method == 'POST':
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Missing data'}), 400
        
        required_fields = ['first_name', 'last_name', 'username', 'password', 'email']
        missing_field = next((field for field in required_fields if field not in data), None)
        if missing_field:
            return jsonify({'error': f'Missing {missing_field}'}), 400

        [first_name, last_name, username, password, email] = [data.get(field) for field in required_fields]

        fields = [
            (first_name, lambda value: validate_name(value, 'First name')),
            (last_name, lambda value: validate_name(value, 'Last name')),
            (username, validate_username),
            (password, validate_password),
            (email, validate_email),
        ]

        for value, validator in fields:
            if (is_valid := validator(value)) is not True:
                return jsonify({'error': is_valid}), 400
                
        hashed_password = hash_password(password)
        
        response, response_code = verify_if_user_exists(username, email)
        if response:
            return jsonify({'error': response}), response_code

        return add_user(first_name=first_name, last_name=last_name, username=username, password=hashed_password, email=email)
    
    return jsonify({'error': 'Invalid request method'}), 405

@app.route('/auth/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Missing data'}), 400
        
        required_fields = ['username', 'password']
        missing_field = next((field for field in required_fields if field not in data or data[field] == ''), None)
        if missing_field:
            return jsonify({'error': f'Missing {missing_field}'}), 400
        
        username = data.get('username')
        password = data.get('password')

        db = SessionLocal()
        user = db.query(User).filter(User.username == username).first()
        db.close()
        if not user:
            return jsonify({'error': 'Invalid username'}), 400
        if check_password(password, user.password):
            token = generate_token(user)
            return jsonify({'message': 'Login successful', 'token': token}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
        
    return jsonify({'error': 'Invalid request method'}), 405


if __name__ == '__main__':
    app.run()
    