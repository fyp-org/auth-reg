from fastapi import HTTPException
from sqlalchemy.orm import Session
import crud


def authenticate_user(db: Session, email: str, password: str):
    user = crud.get_user_by_email(db, email)
    if user is None or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
