import os
from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import schemas
import database
import auth
import crud

load_dotenv()
app = FastAPI()

API_KEY = os.getenv("KEY_REGLOG")

# Получение сессии с БД
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Функция для проверки API ключа
def verify_api_key(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    db_user = auth.authenticate_user(db, user.email, user.password)
    return {"message": f"Welcome {db_user.name}"}

"""
uvicorn main:app --reload
"""