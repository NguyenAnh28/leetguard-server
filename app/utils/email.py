import smtplib
from email.mime.text import MIMEText
import os

def send_verification_email(recipient_email: str, code: str):
    print(f"[DEV] Verification code for {recipient_email}: {code}")  # For local testing
    # These should be set in your environment or config
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.example.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', 'your_username')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'your_password')
    FROM_EMAIL = os.getenv('FROM_EMAIL', 'no-reply@example.com')

    subject = 'Your Verification Code'
    body = f'Your verification code is: {code}'
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, [recipient_email], msg.as_string())
    except Exception as e:
        print(f"[DEV] Email sending failed: {e}") 