from sqlalchemy import Column, Integer, String, DateTime, Boolean
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
    is_verified = Column(Boolean, default=False)  # Whether the user's email is verified
    verification_code = Column(String, nullable=True)  # 6-digit email verification code
    verification_code_expires = Column(DateTime(timezone=True), nullable=True)  # Expiration time for the code
    resend_cooldown_seconds = Column(Integer, default=30)  # Cooldown in seconds for resending code
    last_code_sent_at = Column(DateTime(timezone=True), nullable=True)  # Last time a code was sent