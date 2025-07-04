#!/usr/bin/env python3
"""
Integration tests for email functionality with real Resend API.
These tests require a valid RESEND_API_KEY to be set in the environment.
"""

import os
import pytest
from unittest.mock import patch
from app.utils.email import send_verification_email, send_password_reset_email, send_welcome_email

class TestEmailIntegration:
    """Integration tests for email functionality."""
    
    @pytest.mark.skipif(
        not os.getenv('RESEND_API_KEY'),
        reason="RESEND_API_KEY not set - skipping real email tests"
    )
    def test_send_verification_email_real(self):
        """Test sending a real verification email (requires RESEND_API_KEY)."""
        # Only run if we have a real API key
        if not os.getenv('RESEND_API_KEY'):
            pytest.skip("RESEND_API_KEY not set")
        
        # Test with a real email (you can change this for testing)
        test_email = os.getenv('TEST_EMAIL', 'test@example.com')
        
        success = send_verification_email(test_email, "123456")
        assert success is True
    
    @pytest.mark.skipif(
        not os.getenv('RESEND_API_KEY'),
        reason="RESEND_API_KEY not set - skipping real email tests"
    )
    def test_send_welcome_email_real(self):
        """Test sending a real welcome email (requires RESEND_API_KEY)."""
        if not os.getenv('RESEND_API_KEY'):
            pytest.skip("RESEND_API_KEY not set")
        
        test_email = os.getenv('TEST_EMAIL', 'test@example.com')
        
        success = send_welcome_email(test_email, "test@example.com")
        assert success is True
    
    @pytest.mark.skipif(
        not os.getenv('RESEND_API_KEY'),
        reason="RESEND_API_KEY not set - skipping real email tests"
    )
    def test_send_password_reset_email_real(self):
        """Test sending a real password reset email (requires RESEND_API_KEY)."""
        if not os.getenv('RESEND_API_KEY'):
            pytest.skip("RESEND_API_KEY not set")
        
        test_email = os.getenv('TEST_EMAIL', 'test@example.com')
        
        success = send_password_reset_email(
            test_email, 
            "reset_token_123", 
            "https://example.com/reset"
        )
        assert success is True
    
    def test_email_configuration(self):
        """Test that email configuration is properly set up."""
        # Check required environment variables
        required_vars = ['RESEND_API_KEY', 'FROM_EMAIL']
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            pytest.skip(f"Missing environment variables: {', '.join(missing_vars)}")
        
        # Test that we can import the email module
        try:
            from app.utils.email import send_verification_email
            assert callable(send_verification_email)
        except ImportError as e:
            pytest.fail(f"Failed to import email module: {e}")
    
    @patch('app.utils.email.resend')
    def test_email_failure_handling(self, mock_resend):
        """Test that email failures are handled gracefully."""
        # Mock a failure
        mock_resend.emails.send.side_effect = Exception("API Error")
        
        # Test that failure returns False
        result = send_verification_email("test@example.com", "123456")
        assert result is False
    
    def test_email_template_content(self):
        """Test that email templates contain expected content."""
        with patch('app.utils.email.resend') as mock_resend:
            mock_resend.emails.send.return_value = None
            
            # Test verification email
            send_verification_email("test@example.com", "123456")
            call_args = mock_resend.emails.send.call_args[0][0]
            
            # Check required fields
            assert "to" in call_args
            assert "subject" in call_args
            assert "html" in call_args
            assert "text" in call_args
            assert "from" in call_args
            
            # Check content
            assert "123456" in call_args["html"]
            assert "LeetGuard" in call_args["html"]
            assert call_args["subject"] == "Verify Your Email - LeetGuard"

def test_email_setup_manual():
    """
    Manual test function for email setup verification.
    Run this function to test your email configuration.
    """
    import sys
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Check if required environment variables are set
    required_vars = ['RESEND_API_KEY', 'FROM_EMAIL']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file")
        return False
    
    print("✅ Environment variables are set")
    
    # Test email import
    try:
        from app.utils.email import send_verification_email
        print("✅ Email module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import email module: {e}")
        return False
    
    # Test sending a verification email
    test_email = input("Enter your email address to send a test verification code: ").strip()
    
    if not test_email:
        print("❌ No email address provided")
        return False
    
    print(f"📧 Sending test verification email to {test_email}...")
    
    try:
        success = send_verification_email(test_email, "123456")
        if success:
            print("✅ Test email sent successfully!")
            print("Check your email inbox for the verification code")
            return True
        else:
            print("❌ Failed to send test email")
            return False
    except Exception as e:
        print(f"❌ Error sending test email: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Email Integration")
    print("=" * 40)
    
    success = test_email_setup_manual()
    
    if success:
        print("\n🎉 Email integration is working correctly!")
    else:
        print("\n💥 Email integration test failed!")
        print("\nTroubleshooting tips:")
        print("1. Make sure you have a valid RESEND_API_KEY")
        print("2. Verify your FROM_EMAIL is configured in Resend")
        print("3. Check that you've added your domain to Resend")
        print("4. For testing, you can use the sandbox domain") 