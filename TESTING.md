# Testing Guide for LeetGuard Server

This document explains how to run and maintain the test suite for the LeetGuard Server.

## Test Structure

```
tests/
├── conftest.py                    # Pytest configuration and fixtures
├── unit/                          # Unit tests (fast, no external deps)
│   ├── test_auth.py              # Authentication logic tests
│   └── test_email.py             # Email utility tests
├── integration/                   # Integration tests (with database)
│   ├── test_auth_endpoints.py    # API endpoint tests
│   └── test_email_integration.py # Email integration tests
└── e2e/                          # End-to-end tests (future)
```

## Test Categories

### Unit Tests (`tests/unit/`)

- **Purpose**: Test individual functions and classes in isolation
- **Dependencies**: None (mocked)
- **Speed**: Fast (< 1 second)
- **Coverage**: Business logic, utilities, helpers

**Examples:**

- Password hashing and verification
- JWT token creation/decoding
- Email template generation
- Data validation

### Integration Tests (`tests/integration/`)

- **Purpose**: Test API endpoints and database interactions
- **Dependencies**: Test database (SQLite), mocked external services
- **Speed**: Medium (1-5 seconds)
- **Coverage**: API endpoints, database operations, email sending

**Examples:**

- User registration flow
- Login/logout process
- Email verification
- Rate limiting

### End-to-End Tests (`tests/e2e/`)

- **Purpose**: Test complete user workflows
- **Dependencies**: Full application stack
- **Speed**: Slow (10+ seconds)
- **Coverage**: Complete user journeys

**Examples:**

- Complete signup → verify → login flow
- Password reset process
- User profile management

## Running Tests

### Prerequisites

1. **Install test dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up test environment:**
   ```bash
   # Copy your .env file for testing
   cp .env .env.test
   ```

### Quick Commands

```bash
# Run all tests
python run_tests.py all

# Run specific test types
python run_tests.py unit
python run_tests.py integration
python run_tests.py email

# Run with coverage
python run_tests.py coverage

# Manual email test
python run_tests.py manual-email
```

### Manual Commands

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/unit/test_auth.py -v

# Run specific test class
pytest tests/unit/test_auth.py::TestPasswordHashing -v

# Run specific test method
pytest tests/unit/test_auth.py::TestPasswordHashing::test_password_verification -v

# Run tests with markers
pytest -m unit
pytest -m integration
pytest -m email

# Run tests with coverage
coverage run -m pytest tests/
coverage report
coverage html  # Creates htmlcov/index.html
```

## Test Configuration

### Pytest Configuration (`pytest.ini`)

- Test discovery patterns
- Default options
- Custom markers

### Test Fixtures (`tests/conftest.py`)

- Database setup/teardown
- Test client creation
- Mock data generation
- Environment variable management

### Environment Variables for Testing

```bash
# Required for all tests
SECRET_KEY=test-secret-key
REFRESH_SECRET_KEY=test-refresh-secret-key
DATABASE_URL=sqlite:///./test.db

# Required for email tests
RESEND_API_KEY=your-resend-api-key
FROM_EMAIL=test@example.com
FRONTEND_URL=https://test.com

# Optional for real email testing
TEST_EMAIL=your-email@example.com
```

## Writing Tests

### Unit Test Example

```python
def test_password_verification(self, db_session):
    """Test that password verification works correctly."""
    # Arrange
    user_data = UserCreate(email="test@example.com", password="testpassword123")
    user = create_user(db_session, user_data)

    # Act & Assert
    assert verify_password("testpassword123", user.hashed_password) is True
    assert verify_password("wrongpassword", user.hashed_password) is False
```

### Integration Test Example

```python
@patch('app.utils.email.send_verification_email')
def test_user_signup_success(self, mock_send_email, client, test_user_data):
    """Test successful user signup."""
    # Arrange
    mock_send_email.return_value = True

    # Act
    response = client.post("/auth/signup", json=test_user_data)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert "password" not in data
    mock_send_email.assert_called_once()
```

### Test Best Practices

1. **Use descriptive test names** that explain what is being tested
2. **Follow AAA pattern**: Arrange, Act, Assert
3. **Test one thing per test method**
4. **Use fixtures for common setup**
5. **Mock external dependencies**
6. **Test both success and failure cases**
7. **Use meaningful assertions**

### Test Markers

```python
@pytest.mark.unit
def test_unit_function():
    pass

@pytest.mark.integration
def test_integration_function():
    pass

@pytest.mark.email
def test_email_function():
    pass

@pytest.mark.slow
def test_slow_function():
    pass
```

## Test Data Management

### Fixtures for Common Data

```python
@pytest.fixture
def test_user_data():
    return {
        "email": "test@example.com",
        "password": "testpassword123"
    }

@pytest.fixture
def test_verification_data():
    return {
        "email": "test@example.com",
        "code": "123456"
    }
```

### Database Cleanup

Tests automatically clean up the database between runs using SQLite in-memory database.

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python run_tests.py all
```

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure you're in the project root directory
2. **Database errors**: Check that test database URL is set correctly
3. **Email test failures**: Verify RESEND_API_KEY is set for real email tests
4. **Slow tests**: Use `-m "not slow"` to skip slow tests during development

### Debugging Tests

```bash
# Run with more verbose output
pytest -vvv tests/

# Run with print statements visible
pytest -s tests/

# Run with debugger
pytest --pdb tests/

# Run specific failing test
pytest tests/unit/test_auth.py::TestPasswordHashing::test_password_verification -vvv
```

## Coverage Reports

```bash
# Generate coverage report
coverage run -m pytest tests/
coverage report

# Generate HTML coverage report
coverage html
# Open htmlcov/index.html in browser
```

## Performance Testing

For performance-critical code, consider adding benchmarks:

```python
import time

def test_performance():
    start_time = time.time()
    # Run operation
    end_time = time.time()
    assert (end_time - start_time) < 0.1  # Should complete in < 100ms
```

## Security Testing

Consider adding security-focused tests:

```python
def test_sql_injection_prevention():
    malicious_input = "'; DROP TABLE users; --"
    # Test that malicious input is handled safely

def test_xss_prevention():
    malicious_input = "<script>alert('xss')</script>"
    # Test that malicious input is escaped
```

## Future Improvements

1. **Add E2E tests** for complete user workflows
2. **Add performance benchmarks** for critical paths
3. **Add security tests** for common vulnerabilities
4. **Add load testing** for API endpoints
5. **Add visual regression tests** for email templates
