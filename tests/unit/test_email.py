"""
Unit tests for email functionality.
"""
import pytest
from unittest.mock import patch, MagicMock
from app.utils.email import send_verification_email, send_password_reset_email, send_welcome_email

class TestEmailFunctions:
    """Test email sending functions."""
    
    @patch('app.utils.email.resend')
    def test_send_verification_email_success(self, mock_resend):
        """Test successful verification email sending."""
        # Mock successful response
        mock_response = MagicMock()
        mock_resend.emails.send.return_value = mock_response
        
        # Test sending email
        result = send_verification_email("test@example.com", "123456")
        
        # Should return True on success
        assert result is True
        
        # Verify Resend was called correctly
        mock_resend.emails.send.assert_called_once()
        call_args = mock_resend.emails.send.call_args[0][0]
        assert call_args["to"] == ["test@example.com"]
        assert call_args["subject"] == "Verify Your Email - LeetGuard"
        assert "123456" in call_args["html"]
        assert "123456" in call_args["text"]
    
    @patch('app.utils.email.resend')
    def test_send_verification_email_failure(self, mock_resend):
        """Test verification email sending failure."""
        # Mock failure
        mock_resend.emails.send.side_effect = Exception("API Error")
        
        # Test sending email
        result = send_verification_email("test@example.com", "123456")
        
        # Should return False on failure
        assert result is False
    
    @patch('app.utils.email.resend')
    def test_send_password_reset_email_success(self, mock_resend):
        """Test successful password reset email sending."""
        # Mock successful response
        mock_response = MagicMock()
        mock_resend.emails.send.return_value = mock_response
        
        # Test sending email
        result = send_password_reset_email("test@example.com", "reset_token_123", "https://example.com/reset")
        
        # Should return True on success
        assert result is True
        
        # Verify Resend was called correctly
        mock_resend.emails.send.assert_called_once()
        call_args = mock_resend.emails.send.call_args[0][0]
        assert call_args["to"] == ["test@example.com"]
        assert call_args["subject"] == "Reset Your Password - LeetGuard"
        assert "reset_token_123" in call_args["html"]
        assert "https://example.com/reset?token=reset_token_123" in call_args["html"]
    
    @patch('app.utils.email.resend')
    def test_send_welcome_email_success(self, mock_resend):
        """Test successful welcome email sending."""
        # Mock successful response
        mock_response = MagicMock()
        mock_resend.emails.send.return_value = mock_response
        
        # Test sending email
        result = send_welcome_email("test@example.com", "test@example.com")
        
        # Should return True on success
        assert result is True
        
        # Verify Resend was called correctly
        mock_resend.emails.send.assert_called_once()
        call_args = mock_resend.emails.send.call_args[0][0]
        assert call_args["to"] == ["test@example.com"]
        assert call_args["subject"] == "Welcome to LeetGuard!"
        assert "test@example.com" in call_args["html"]
    
    def test_email_templates_contain_required_content(self):
        """Test that email templates contain required content."""
        # Test verification email template
        with patch('app.utils.email.resend') as mock_resend:
            mock_resend.emails.send.return_value = MagicMock()
            send_verification_email("test@example.com", "123456")
            
            call_args = mock_resend.emails.send.call_args[0][0]
            html_content = call_args["html"]
            text_content = call_args["text"]
            
            # Check for required content
            assert "LeetGuard" in html_content
            assert "123456" in html_content
            assert "Verify Your Email" in html_content
            assert "123456" in text_content
            assert "LeetGuard" in text_content
    
    def test_password_reset_email_contains_reset_link(self):
        """Test that password reset email contains the reset link."""
        with patch('app.utils.email.resend') as mock_resend:
            mock_resend.emails.send.return_value = MagicMock()
            send_password_reset_email("test@example.com", "token123", "https://example.com/reset")
            
            call_args = mock_resend.emails.send.call_args[0][0]
            html_content = call_args["html"]
            text_content = call_args["text"]
            
            # Check for reset link
            assert "https://example.com/reset?token=token123" in html_content
            assert "https://example.com/reset?token=token123" in text_content
            assert "Reset Password" in html_content 