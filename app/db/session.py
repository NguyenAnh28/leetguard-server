# Sets up the database connection and session for the app. Handles connecting to the database and creating tables.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

try:
    engine = create_engine(settings.DATABASE_URL)
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