# Sets up the database connection and session for the app. Handles connecting to the database and creating tables.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os 
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    engine = create_engine(DATABASE_URL)
except Exception as e:
    print(f"Database connection failed: {e}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from app.models.user import Base
Base.metadata.create_all(bind=engine)

# Dependency for getting a database session. Use with FastAPI Depends.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()