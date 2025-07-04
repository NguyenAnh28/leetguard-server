"""
Integration tests for authentication endpoints.
"""
import pytest
from fastapi import status
from unittest.mock import patch

class TestAuthEndpoints:
    """Test authentication API endpoints."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "ok"}
    
    @patch('app.utils.email.send_verification_email')
    def test_user_signup_success(self, mock_send_email, client, test_user_data):
        """Test successful user signup."""
        mock_send_email.return_value = True
        
        response = client.post("/auth/signup", json=test_user_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["user"]["email"] == test_user_data["email"]
        assert "id" in data["user"]
        assert "password" not in data["user"]  # Password should not be returned
        assert data["email_sent"] is True
        assert "successfully" in data["message"]
        
        # Verify email was sent
        mock_send_email.assert_called_once()
    
    @patch('app.utils.email.send_verification_email')
    def test_user_signup_email_failure(self, mock_send_email, client, test_user_data):
        """Test user signup when email sending fails."""
        mock_send_email.return_value = False
        
        response = client.post("/auth/signup", json=test_user_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["user"]["email"] == test_user_data["email"]
        assert "id" in data["user"]
        assert data["email_sent"] is False
        assert "couldn't send" in data["message"]
        assert "resend" in data["message"]
        
        # Verify email was attempted
        mock_send_email.assert_called_once()
    
    def test_user_signup_duplicate_email(self, client, test_user_data):
        """Test signup with existing email."""
        # First signup
        with patch('app.utils.email.send_verification_email') as mock_send_email:
            mock_send_email.return_value = True
            response = client.post("/auth/signup", json=test_user_data)
            assert response.status_code == status.HTTP_200_OK
        
        # Second signup with same email
        with patch('app.utils.email.send_verification_email') as mock_send_email:
            mock_send_email.return_value = True
            response = client.post("/auth/signup", json=test_user_data)
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert "Email already registered" in response.json()["detail"]
    
    def test_user_signup_invalid_email(self, client):
        """Test signup with invalid email format."""
        invalid_user_data = {
            "email": "invalid-email",
            "password": "password123"
        }
        
        response = client.post("/auth/signup", json=invalid_user_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_user_login_unverified(self, client, test_user_data):
        """Test login with unverified email."""
        # Create user
        with patch('app.utils.email.send_verification_email') as mock_send_email:
            mock_send_email.return_value = True
            client.post("/auth/signup", json=test_user_data)
        
        # Try to login
        login_data = {
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
        response = client.post("/auth/login", data=login_data)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Please verify your email" in response.json()["detail"]
    
    def test_user_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        login_data = {
            "username": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        response = client.post("/auth/login", data=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid credentials" in response.json()["detail"]
    
    @patch('app.utils.email.send_verification_email')
    @patch('app.utils.email.send_welcome_email')
    def test_email_verification_success(self, mock_welcome_email, mock_verification_email, client, test_user_data):
        """Test successful email verification."""
        mock_verification_email.return_value = True
        mock_welcome_email.return_value = True
        
        # Create user
        response = client.post("/auth/signup", json=test_user_data)
        assert response.status_code == status.HTTP_200_OK
        
        # Get verification code from the created user
        from app.crud.user import get_user_by_email
        from app.db.session import SessionLocal
        db = SessionLocal()
        user = get_user_by_email(db, test_user_data["email"])
        db.close()
        
        # Verify email
        verification_data = {
            "email": test_user_data["email"],
            "code": user.verification_code
        }
        response = client.post("/auth/verify-email-code", json=verification_data)
        
        assert response.status_code == status.HTTP_200_OK
        assert "Email verified successfully" in response.json()["message"]
        
        # Verify welcome email was sent
        mock_welcome_email.assert_called_once()
    
    @patch('app.utils.email.send_verification_email')
    def test_email_verification_invalid_code(self, mock_send_email, client, test_user_data):
        """Test email verification with invalid code."""
        mock_send_email.return_value = True
        
        # Create user
        response = client.post("/auth/signup", json=test_user_data)
        assert response.status_code == status.HTTP_200_OK
        
        # Try to verify with wrong code
        verification_data = {
            "email": test_user_data["email"],
            "code": "000000"
        }
        response = client.post("/auth/verify-email-code", json=verification_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid or expired verification code" in response.json()["detail"]
    
    @patch('app.utils.email.send_verification_email')
    def test_resend_verification_code(self, mock_send_email, client, test_user_data):
        """Test resending verification code."""
        mock_send_email.return_value = True
        
        # Create user
        response = client.post("/auth/signup", json=test_user_data)
        assert response.status_code == status.HTTP_200_OK
        
        # Resend verification code
        resend_data = {
            "email": test_user_data["email"],
            "code": "000000"  # Code doesn't matter for resend
        }
        response = client.post("/auth/resend-verification-code", json=resend_data)
        
        assert response.status_code == status.HTTP_200_OK
        assert "Verification code resent successfully" in response.json()["message"]
        
        # Verify email was sent again
        assert mock_send_email.call_count == 2  # Once for signup, once for resend
    
    @patch('app.utils.email.send_verification_email')
    def test_resend_verification_code_failure(self, mock_send_email, client, test_user_data):
        """Test resending verification code when email fails."""
        # First call succeeds (signup), second call fails (resend)
        mock_send_email.side_effect = [True, False]
        
        # Create user
        response = client.post("/auth/signup", json=test_user_data)
        assert response.status_code == status.HTTP_200_OK
        
        # Try to resend verification code
        resend_data = {
            "email": test_user_data["email"],
            "code": "000000"
        }
        response = client.post("/auth/resend-verification-code", json=resend_data)
        
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Failed to send verification email" in response.json()["detail"]
    
    @patch('app.utils.email.send_verification_email')
    @patch('app.utils.email.send_welcome_email')
    def test_complete_auth_flow(self, mock_welcome_email, mock_verification_email, client, test_user_data):
        """Test complete authentication flow: signup -> verify -> login."""
        mock_verification_email.return_value = True
        mock_welcome_email.return_value = True
        
        # 1. Signup
        response = client.post("/auth/signup", json=test_user_data)
        assert response.status_code == status.HTTP_200_OK
        
        # 2. Get verification code
        from app.crud.user import get_user_by_email
        from app.db.session import SessionLocal
        db = SessionLocal()
        user = get_user_by_email(db, test_user_data["email"])
        db.close()
        
        # 3. Verify email
        verification_data = {
            "email": test_user_data["email"],
            "code": user.verification_code
        }
        response = client.post("/auth/verify-email-code", json=verification_data)
        assert response.status_code == status.HTTP_200_OK
        
        # 4. Login
        login_data = {
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
        response = client.post("/auth/login", data=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer" 