from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine instance
engine = create_engine(DATABASE_URL)

# Create a factory for generating new database sessions
SessionLocal = sessionmaker(bind=engine)

# All database models (tables) will inherit from this base class
Base = declarative_base()


def get_db():
    # Create a new database session
    db = SessionLocal()
    try:
        # Yield the session to be used in the API endpoint
        # "Here's your database connection, but remember to give it back!"
        yield db
    finally:
        db.close()
