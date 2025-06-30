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
   DATABASE_URL=postgresql://leetguard_user:yourpassword@localhost:5432/leetguard
   SECRET_KEY=your_secret_key
   ```
5. Make sure PostgreSQL is running and database/user created.

## Run server

```bash
uvicorn app.main:app --reload
```

Server runs on http://127.0.0.1:8000

## API

- `GET /health` — health check
- `POST /auth/signup` — signup
- `POST /auth/login` — login

## Testing

```bash
pytest
```

## License

MIT License © Your Name
