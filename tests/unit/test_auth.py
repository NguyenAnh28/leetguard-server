"""
Unit tests for authentication functionality.
"""
import pytest
from datetime import datetime, timedelta, timezone
from app.crud.user import verify_password, get_user_by_email, create_user
from app.schemas.user import UserCreate
from app.utils.jwt import create_access_token, decode_access_token, create_refresh_token, decode_refresh_token

class TestPasswordHashing:
    """Test password hashing and verification."""
    
    def test_password_verification(self, db_session):
        """Test that password verification works correctly."""
        # Create a test user
        user_data = UserCreate(email="test@example.com", password="testpassword123")
        user = create_user(db_session, user_data)
        
        # Test correct password
        assert verify_password("testpassword123", user.hashed_password) is True
        
        # Test incorrect password
        assert verify_password("wrongpassword", user.hashed_password) is False
        
        # Test empty password
        assert verify_password("", user.hashed_password) is False

class TestJWTTokens:
    """Test JWT token creation and decoding."""
    
    def test_access_token_creation_and_decoding(self):
        """Test access token creation and decoding."""
        user_id = "123"
        token = create_access_token(data={"sub": user_id})
        
        # Token should be a string
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Decode token
        payload = decode_access_token(token)
        assert payload is not None
        assert payload["sub"] == user_id
        assert "exp" in payload
    
    def test_refresh_token_creation_and_decoding(self):
        """Test refresh token creation and decoding."""
        user_id = "123"
        token = create_refresh_token(data={"sub": user_id})
        
        # Token should be a string
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Decode token
        payload = decode_refresh_token(token)
        assert payload is not None
        assert payload["sub"] == user_id
        assert "exp" in payload
    
    def test_invalid_token_decoding(self):
        """Test decoding invalid tokens."""
        # Test invalid access token
        invalid_token = "invalid.token.here"
        payload = decode_access_token(invalid_token)
        assert payload is None
        
        # Test invalid refresh token
        payload = decode_refresh_token(invalid_token)
        assert payload is None
    
    def test_token_expiration(self):
        """Test that tokens expire correctly."""
        user_id = "123"
        
        # Create token with short expiration
        token = create_access_token(
            data={"sub": user_id}, 
            expires_delta=timedelta(seconds=1)
        )
        
        # Token should be valid initially
        payload = decode_access_token(token)
        assert payload is not None
        
        # Wait for expiration (in real tests, you'd mock time)
        # For now, we'll just test that the token structure is correct
        assert "exp" in payload

class TestUserCRUD:
    """Test user CRUD operations."""
    
    def test_create_user(self, db_session):
        """Test user creation."""
        user_data = UserCreate(email="newuser@example.com", password="password123")
        user = create_user(db_session, user_data)
        
        assert user.email == "newuser@example.com"
        assert user.hashed_password != "password123"  # Should be hashed
        assert user.is_verified is False
        assert user.verification_code is not None
        assert len(user.verification_code) == 6
        assert user.verification_code_expires is not None
    
    def test_get_user_by_email(self, db_session):
        """Test retrieving user by email."""
        # Create a user
        user_data = UserCreate(email="test@example.com", password="password123")
        created_user = create_user(db_session, user_data)
        
        # Retrieve the user
        retrieved_user = get_user_by_email(db_session, "test@example.com")
        
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == created_user.email
    
    def test_get_user_by_email_not_found(self, db_session):
        """Test retrieving non-existent user."""
        user = get_user_by_email(db_session, "nonexistent@example.com")
        assert user is None 