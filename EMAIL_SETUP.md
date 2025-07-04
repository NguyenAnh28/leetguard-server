# Email Service Setup Guide

This guide will help you set up a production-ready email service for LeetGuard using Resend.

## Why Resend?

- **Free Tier**: 3,000 emails/month
- **Excellent Deliverability**: 99.9%+ delivery rate
- **Modern API**: Simple, developer-friendly
- **Real-time Analytics**: Track email performance
- **Domain Verification**: Easy domain setup

## Step 1: Sign Up for Resend

1. Go to [resend.com](https://resend.com)
2. Click "Get Started" and create a free account
3. Verify your email address

## Step 2: Get Your API Key

1. In the Resend dashboard, go to "API Keys"
2. Click "Create API Key"
3. Give it a name (e.g., "LeetGuard Production")
4. Copy the API key (starts with `re_`)

## Step 3: Configure Your Domain

### Option A: Use Your Own Domain (Recommended for Production)

1. In Resend dashboard, go to "Domains"
2. Click "Add Domain"
3. Enter your domain (e.g., `yourdomain.com`)
4. Add the required DNS records:

   - **MX Record**: `mxa.resend.com` (Priority: 10)
   - **TXT Record**: `resend-verification=your-verification-code`
   - **CNAME Record**: `resend._domainkey.yourdomain.com` → `resend._domainkey.resend.com`

5. Wait for DNS verification (usually 5-10 minutes)
6. Once verified, you can use `noreply@yourdomain.com` as your FROM_EMAIL

### Option B: Use Sandbox Domain (For Testing)

1. In Resend dashboard, go to "Domains"
2. You'll see a sandbox domain like `sandbox-123456789.resend.com`
3. Use `noreply@sandbox-123456789.resend.com` as your FROM_EMAIL

## Step 4: Update Your Environment Variables

Add these to your `.env` file:

```ini
# Email Service (Resend)
RESEND_API_KEY=re_your_api_key_here
FROM_EMAIL=noreply@yourdomain.com

# Frontend URL (for email links)
FRONTEND_URL=https://yourdomain.com

# JWT Tokens (if not already set)
SECRET_KEY=your_secret_key_here
REFRESH_SECRET_KEY=your_refresh_secret_key_here
```

## Step 5: Test Your Email Setup

Run the test script to verify everything works:

```bash
python test_email.py
```

This will:

1. Check your environment variables
2. Test the email module import
3. Send a test verification email
4. Confirm the setup is working

## Step 6: Install Dependencies

Make sure you have the Resend package installed:

```bash
pip install resend
```

Or update your requirements:

```bash
pip install -r requirements.txt
```

## Email Templates

The application includes three types of emails:

### 1. Verification Email

- Sent when users sign up
- Contains 6-digit verification code
- Expires in 10 minutes
- Beautiful HTML template with LeetGuard branding

### 2. Welcome Email

- Sent after email verification
- Welcomes users to the platform
- Includes next steps and features
- Professional onboarding experience

### 3. Password Reset Email (Ready for Implementation)

- Template ready for password reset functionality
- Secure reset tokens
- 1-hour expiration
- Clear call-to-action buttons

## Production Considerations

### Rate Limiting

- Verification codes have progressive cooldowns: 30s → 60s → 120s → 240s
- Maximum 5 resend attempts per user
- Prevents email abuse

### Error Handling

- Email failures don't break user registration
- Graceful degradation with logging
- Clear error messages for users

### Monitoring

- All email sends are logged
- Failed sends are tracked
- Use Resend dashboard for delivery analytics

### Security

- API keys are environment variables
- No hardcoded credentials
- Secure token generation
- Email verification required for login

## Troubleshooting

### Common Issues

1. **"Invalid API Key"**

   - Check your RESEND_API_KEY is correct
   - Ensure no extra spaces or characters

2. **"Domain not verified"**

   - Wait for DNS propagation (up to 24 hours)
   - Double-check DNS records
   - Use sandbox domain for testing

3. **"Email not received"**

   - Check spam folder
   - Verify FROM_EMAIL is configured
   - Check Resend dashboard for delivery status

4. **"Module not found"**
   - Run `pip install resend`
   - Check your virtual environment is activated

### Getting Help

- [Resend Documentation](https://resend.com/docs)
- [Resend Support](https://resend.com/support)
- Check the application logs for detailed error messages

## Next Steps

Once email is working, consider implementing:

1. **Password Reset Flow** - Use the existing template
2. **Email Preferences** - Let users control email frequency
3. **Transactional Emails** - Notifications for important events
4. **Email Analytics** - Track open rates and engagement
5. **A/B Testing** - Test different email templates

Your email service is now production-ready! 🎉
