import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is required")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required")
    
    REFRESH_SECRET_KEY: str = os.getenv("REFRESH_SECRET_KEY")
    if not REFRESH_SECRET_KEY:
        raise ValueError("REFRESH_SECRET_KEY environment variable is required")
    
    # Email (Resend)
    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY")
    if not RESEND_API_KEY:
        raise ValueError("RESEND_API_KEY environment variable is required")
    
    FROM_EMAIL: str = os.getenv("FROM_EMAIL", "noreply@leetguard.com")
    
    # Frontend URL for email links
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "https://leetguard.com")
    
    # JWT Settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    # Email verification settings
    VERIFICATION_CODE_EXPIRE_MINUTES: int = int(os.getenv("VERIFICATION_CODE_EXPIRE_MINUTES", "10"))
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = int(os.getenv("PASSWORD_RESET_TOKEN_EXPIRE_HOURS", "1"))
    
    # Rate limiting settings
    INITIAL_RESEND_COOLDOWN_SECONDS: int = int(os.getenv("INITIAL_RESEND_COOLDOWN_SECONDS", "30"))
    MAX_RESEND_ATTEMPTS: int = int(os.getenv("MAX_RESEND_ATTEMPTS", "5"))
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"

# Create settings instance
settings = Settings() 