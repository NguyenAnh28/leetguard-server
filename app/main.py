from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserOut
from app.schemas.token import Token
from app.crud.user import get_user_by_email, create_user
from app.utils import jwt as jwt_utils
from app.crud.user import verify_password
from app.crud import user as user_crud
from app.utils.jwt import get_current_user

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Health check endpoint. Anyone can access this to check if the server and database are running.
@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    return {"status": "ok"}

# User registration endpoint. Allows anyone to sign up with an email and password.
@app.post("/auth/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return create_user(db, user)

# User login endpoint. Allows registered users to log in and receive access and refresh tokens.
@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not user_crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = jwt_utils.create_access_token(data={"sub": str(user.id)})
    refresh_token = jwt_utils.create_refresh_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# Token refresh endpoint. Allows users to get new access and refresh tokens using a valid refresh token.
@app.post("/auth/refresh", response_model = Token)
def refresh_token(refresh_token: str = Body(...)):
    payload = jwt_utils.decode_refresh_token(refresh_token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    
    user_id = payload.get("sub")
    if user_id is None: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token payload")
    
    access_token = jwt_utils.create_access_token(data={"sub": user_id})
    new_refresh_token = jwt_utils.create_refresh_token(data={"sub": user_id})

    return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}

# Protected endpoint. Returns the current user's information. Requires a valid access token (user must be logged in).
@app.get("/me", response_model=UserOut)
def read_current_user(current_user: UserOut = Depends(get_current_user)):
    return current_user