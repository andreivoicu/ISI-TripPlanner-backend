from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection string
DATABASE_URL = "postgresql://username:password@localhost:5432/user_registration"

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
        password=password,  # Typically, you'd hash the password before storing it
        email=email
    )
    try:
        db.add(new_user)  # Add the user object to the session
        db.commit()  # Commit the transaction to the database
        db.refresh(new_user)  # Refresh the instance to get the new ID from the database
        print(f"User {new_user.username} added successfully!")
    except Exception as e:
        db.rollback()  # In case of error, rollback the transaction
        print(f"Error adding user: {e}")
    finally:
        db.close()  # Always close the session

# Create the tables if they don't exist yet
if __name__ == '__main__':
    create_tables()

    # Example usage: Adding a new user
    add_user(
        first_name='John',
        last_name='Doe',
        username='johndoe',
        password='securepassword123',  # Remember to hash the password in production
        email='johndoe@example.com'
    )
