# API Examples for LeetGuard Server

This document provides examples of API requests and responses for the LeetGuard Server.

## Authentication Endpoints

### 1. User Signup

**Request:**

```bash
POST /auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (Success - Email Sent):**

```json
{
  "user": {
    "id": 1,
    "email": "user@example.com"
  },
  "email_sent": true,
  "message": "Account created successfully! Please check your email for verification code."
}
```

**Response (Success - Email Failed):**

```json
{
  "user": {
    "id": 1,
    "email": "user@example.com"
  },
  "email_sent": false,
  "message": "Account created successfully! However, we couldn't send the verification email. Please use the resend feature or contact support."
}
```

**Response (Error - Duplicate Email):**

```json
{
  "detail": "Email already registered"
}
```

### 2. User Login

**Request:**

```bash
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=securepassword123
```

**Response (Success):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Response (Error - Unverified Email):**

```json
{
  "detail": "Please verify your email before logging in."
}
```

**Response (Error - Invalid Credentials):**

```json
{
  "detail": "Invalid credentials"
}
```

### 3. Email Verification

**Request:**

```bash
POST /auth/verify-email-code
Content-Type: application/json

{
  "email": "user@example.com",
  "code": "123456"
}
```

**Response (Success):**

```json
{
  "message": "Email verified successfully! Welcome to LeetGuard!"
}
```

**Response (Error - Invalid Code):**

```json
{
  "detail": "Invalid or expired verification code."
}
```

### 4. Resend Verification Code

**Request:**

```bash
POST /auth/resend-verification-code
Content-Type: application/json

{
  "email": "user@example.com",
  "code": "000000"
}
```

**Response (Success):**

```json
{
  "message": "Verification code resent successfully. Please check your email."
}
```

**Response (Error - Rate Limited):**

```json
{
  "detail": "You can request a new code in 45 seconds."
}
```

**Response (Error - Email Failed):**

```json
{
  "detail": "Failed to send verification email. Please try again later or contact support if the problem persists."
}
```

### 5. Token Refresh

**Request:**

```bash
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (Success):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 6. Get Current User

**Request:**

```bash
GET /me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (Success):**

```json
{
  "id": 1,
  "email": "user@example.com"
}
```

### 7. Health Check

**Request:**

```bash
GET /health
```

**Response:**

```json
{
  "status": "ok"
}
```

## Error Responses

### Common HTTP Status Codes

- `200 OK` - Request successful
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Invalid or missing authentication
- `403 Forbidden` - Email not verified
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `429 Too Many Requests` - Rate limited
- `500 Internal Server Error` - Server error

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Authentication Flow

### Complete User Registration Flow

1. **Signup**

   ```bash
   POST /auth/signup
   {
     "email": "user@example.com",
     "password": "securepassword123"
   }
   ```

2. **Check Email Status**

   - If `email_sent: true` → Check email for verification code
   - If `email_sent: false` → Use resend feature

3. **Verify Email**

   ```bash
   POST /auth/verify-email-code
   {
     "email": "user@example.com",
     "code": "123456"
   }
   ```

4. **Login**

   ```bash
   POST /auth/login
   username=user@example.com&password=securepassword123
   ```

5. **Use Access Token**
   ```bash
   GET /me
   Authorization: Bearer <access_token>
   ```

## Rate Limiting

The resend verification endpoint implements a fixed 30-second cooldown between requests to prevent abuse.

## Testing with cURL

### Signup Example

```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

### Login Example

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpassword123"
```

### Protected Endpoint Example

```bash
curl -X GET "http://localhost:8000/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Frontend Integration Tips

1. **Handle Email Status**: Always check the `email_sent` field in signup response
2. **Show Clear Messages**: Display the `message` field to users
3. **Implement Resend**: Provide a resend button for failed emails
4. **Rate Limiting**: Show countdown timers for resend cooldowns
5. **Error Handling**: Display user-friendly error messages
6. **Token Management**: Store and refresh tokens appropriately
