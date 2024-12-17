from flask import Flask # type: ignore
from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore
from .models import Base
from dotenv import load_dotenv # type: ignore
from flask_cors import CORS # type: ignore
import os

# Load environment variables from .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Initialize the Flask app
app = Flask(__name__)
CORS(app)
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# Initialize SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables if they do not exist
def create_tables():
    Base.metadata.create_all(bind=engine)

create_tables()

from . import routes  # Import routes to register endpoints