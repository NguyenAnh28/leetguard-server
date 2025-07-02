import os
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, get_db
from app.crud.user import get_user_by_id

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
REFRESH_SECRET_KEY = os.getenv('REFRESH_SECRET_KEY')

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS= 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Creates a JWT access token for a user. Used after successful login to authenticate future requests.
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Decodes and verifies a JWT access token. Returns the payload if valid, otherwise None.
def decode_access_token(token: str):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
        return payload 
    except jwt.PyJWTError:
        return None

# Creates a JWT refresh token for a user. Used to obtain new access tokens without re-authenticating.
def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Decodes and verifies a JWT refresh token. Returns the payload if valid, otherwise None.
def decode_refresh_token(token: str):
    try: 
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None 