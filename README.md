# LeetGuard Server

Backend API for LeetGuard — authentication service using FastAPI and PostgreSQL.

---

## Setup

1. Clone repo
2. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create `.env` file with:

   ```ini
   # Database
   DATABASE_URL=postgresql://leetguard_user:yourpassword@localhost:5432/leetguard

   # JWT Tokens
   SECRET_KEY=your_secret_key_here
   REFRESH_SECRET_KEY=your_refresh_secret_key_here

   # Email Service (Resend)
   RESEND_API_KEY=your_resend_api_key_here
   FROM_EMAIL=noreply@yourdomain.com

   # Frontend URL
   FRONTEND_URL=https://yourdomain.com

   # Optional Settings
   ENVIRONMENT=development
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   VERIFICATION_CODE_EXPIRE_MINUTES=10
   ```

5. Make sure PostgreSQL is running and database/user created.

## Run server

```bash
uvicorn app.main:app --reload
```

Server runs on http://127.0.0.1:8000

## Email Setup

This application uses [Resend](https://resend.com) for sending emails. To set up:

1. Sign up for a free account at [resend.com](https://resend.com)
2. Get your API key from the dashboard
3. Add your domain or use the sandbox domain for testing
4. Set the `RESEND_API_KEY` in your `.env` file

## API

- `GET /health` — health check
- `POST /auth/signup` — signup with email verification (returns email status)
- `POST /auth/login` — login (requires email verification)
- `POST /auth/refresh` — refresh access token
- `GET /me` — get current user info
- `POST /auth/verify-email-code` — verify email with 6-digit code
- `POST /auth/resend-verification-code` — resend verification code

## Testing

The project includes a comprehensive test suite with unit, integration, and end-to-end tests.

### Quick Test Commands

```bash
# Run all tests
python run_tests.py all

# Run specific test types
python run_tests.py unit          # Unit tests only
python run_tests.py integration   # Integration tests only
python run_tests.py email         # Email integration tests

# Run with coverage
python run_tests.py coverage

# Manual email test (requires RESEND_API_KEY)
python run_tests.py manual-email
```

### Test Structure

```
tests/
├── conftest.py                    # Pytest configuration and fixtures
├── unit/                          # Unit tests
│   ├── test_auth.py              # Authentication unit tests
│   └── test_email.py             # Email unit tests
├── integration/                   # Integration tests
│   ├── test_auth_endpoints.py    # API endpoint tests
│   └── test_email_integration.py # Email integration tests
└── e2e/                          # End-to-end tests (future)
```

### Running Tests Manually

```bash
# Run with pytest directly
pytest tests/ -v

# Run specific test file
pytest tests/unit/test_auth.py -v

# Run tests with markers
pytest -m unit
pytest -m integration
pytest -m email
```

### Test Requirements

- **Unit Tests**: No external dependencies, run quickly
- **Integration Tests**: Require test database (SQLite)
- **Email Tests**: Require `RESEND_API_KEY` for real email tests

## License

MIT License © Your Name
