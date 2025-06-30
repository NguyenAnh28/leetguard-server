from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    return {"status": "ok"}