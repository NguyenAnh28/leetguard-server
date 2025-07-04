import logging
from typing import Optional
from resend import Resend
from fastapi import HTTPException, status
from app.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Initialize Resend client
resend = Resend(api_key=settings.RESEND_API_KEY)

def send_verification_email(recipient_email: str, code: str) -> bool:
    """
    Send verification email using Resend.
    
    Args:
        recipient_email: Email address to send to
        code: 6-digit verification code
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # HTML template for verification email
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verify Your Email</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #2563eb; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f8fafc; padding: 30px; border-radius: 0 0 8px 8px; }}
                .code {{ background: #e2e8f0; padding: 15px; text-align: center; font-size: 24px; font-weight: bold; letter-spacing: 3px; border-radius: 6px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #64748b; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>LeetGuard</h1>
                    <p>Verify Your Email Address</p>
                </div>
                <div class="content">
                    <h2>Welcome to LeetGuard!</h2>
                    <p>Thank you for signing up. To complete your registration, please enter the verification code below:</p>
                    
                    <div class="code">{code}</div>
                    
                    <p><strong>This code will expire in 10 minutes.</strong></p>
                    
                    <p>If you didn't create an account with LeetGuard, you can safely ignore this email.</p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 LeetGuard. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        text_content = f"""
        Welcome to LeetGuard!
        
        Thank you for signing up. To complete your registration, please enter the verification code below:
        
        {code}
        
        This code will expire in 10 minutes.
        
        If you didn't create an account with LeetGuard, you can safely ignore this email.
        
        © 2024 LeetGuard. All rights reserved.
        """
        
        # Send email via Resend
        response = resend.emails.send({
            "from": settings.FROM_EMAIL,
            "to": [recipient_email],
            "subject": "Verify Your Email - LeetGuard",
            "html": html_content,
            "text": text_content
        })
        
        logger.info(f"Verification email sent successfully to {recipient_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send verification email to {recipient_email}: {str(e)}")
        return False

def send_password_reset_email(recipient_email: str, reset_token: str, reset_url: str) -> bool:
    """
    Send password reset email using Resend.
    
    Args:
        recipient_email: Email address to send to
        reset_token: Password reset token
        reset_url: URL for password reset
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # HTML template for password reset email
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reset Your Password</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #dc2626; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f8fafc; padding: 30px; border-radius: 0 0 8px 8px; }}
                .button {{ display: inline-block; background: #dc2626; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #64748b; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>LeetGuard</h1>
                    <p>Reset Your Password</p>
                </div>
                <div class="content">
                    <h2>Password Reset Request</h2>
                    <p>We received a request to reset your password. Click the button below to create a new password:</p>
                    
                    <a href="{reset_url}?token={reset_token}" class="button">Reset Password</a>
                    
                    <p><strong>This link will expire in 1 hour.</strong></p>
                    
                    <p>If you didn't request a password reset, you can safely ignore this email. Your password will remain unchanged.</p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 LeetGuard. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        text_content = f"""
        Password Reset Request
        
        We received a request to reset your password. Click the link below to create a new password:
        
        {reset_url}?token={reset_token}
        
        This link will expire in 1 hour.
        
        If you didn't request a password reset, you can safely ignore this email. Your password will remain unchanged.
        
        © 2024 LeetGuard. All rights reserved.
        """
        
        # Send email via Resend
        response = resend.emails.send({
            "from": settings.FROM_EMAIL,
            "to": [recipient_email],
            "subject": "Reset Your Password - LeetGuard",
            "html": html_content,
            "text": text_content
        })
        
        logger.info(f"Password reset email sent successfully to {recipient_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send password reset email to {recipient_email}: {str(e)}")
        return False

def send_welcome_email(recipient_email: str, username: str) -> bool:
    """
    Send welcome email to newly verified users.
    
    Args:
        recipient_email: Email address to send to
        username: User's email/username
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # HTML template for welcome email
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome to LeetGuard!</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #059669; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f8fafc; padding: 30px; border-radius: 0 0 8px 8px; }}
                .button {{ display: inline-block; background: #059669; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #64748b; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>LeetGuard</h1>
                    <p>Welcome to the Community!</p>
                </div>
                <div class="content">
                    <h2>Welcome, {username}!</h2>
                    <p>Your email has been successfully verified. You're now ready to start your coding journey with LeetGuard!</p>
                    
                    <a href="{settings.FRONTEND_URL}" class="button">Get Started</a>
                    
                    <p>Here's what you can do next:</p>
                    <ul>
                        <li>Complete your profile</li>
                        <li>Start solving coding challenges</li>
                        <li>Join our community discussions</li>
                        <li>Track your progress</li>
                    </ul>
                    
                    <p>If you have any questions, feel free to reach out to our support team.</p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 LeetGuard. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        text_content = f"""
        Welcome to LeetGuard!
        
        Welcome, {username}!
        
        Your email has been successfully verified. You're now ready to start your coding journey with LeetGuard!
        
        Visit us at: {settings.FRONTEND_URL}
        
        Here's what you can do next:
        - Complete your profile
        - Start solving coding challenges
        - Join our community discussions
        - Track your progress
        
        If you have any questions, feel free to reach out to our support team.
        
        © 2024 LeetGuard. All rights reserved.
        """
        
        # Send email via Resend
        response = resend.emails.send({
            "from": settings.FROM_EMAIL,
            "to": [recipient_email],
            "subject": "Welcome to LeetGuard!",
            "html": html_content,
            "text": text_content
        })
        
        logger.info(f"Welcome email sent successfully to {recipient_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send welcome email to {recipient_email}: {str(e)}")
        return False 