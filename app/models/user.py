from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# SQLAlchemy model representing a user in the system. Stores user ID, email, hashed password, and account creation time.
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # Unique user ID
    email = Column(String, unique=True, index=True, nullable=False)  # User's email address
    hashed_password = Column(String, nullable=False)  # Hashed password for authentication
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Timestamp of account creation