import os
import datetime
from datetime import timezone, timedelta

from fastapi import FastAPI, Depends, HTTPException, Header, Response, Cookie
# for cross-domain headers
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import jwt

import schemas
import database
import auth
import crud

load_dotenv()

app = FastAPI()

# Параметры для API ключа и JWT
API_KEY = os.getenv("KEY_REGLOG")
JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret_here")
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_HOURS = 1

"""НЕ ИСПОЛЬЗОВАТЬ НАХУЙ В ПРОДЕ, ПОИСКАТЬ УМНОЕ РЕШЕНИЕ"""
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],        # разрешённые источники запросов
    allow_credentials = True,       # разрешить печеньки
    allow_methods=["*"],            # разрешить все HTTP МЕТОДЫ
    allow_headers=["*"],            # разрешить все заголовки

)




# Получение сессии с БД
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Проверка API ключа
def verify_api_key(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

# Регистрация пользователя
@app.post("/register", response_model=schemas.UserResponse)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# Логин пользователя с выдачей JWT токена
@app.post("/login")
def login(
    user: schemas.UserLogin,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    # Аутентификация пользователя (функция должна проверить email и password)
    db_user = auth.authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Задаём время истечения токена (1 час)
    expiration_time = datetime.datetime.now(timezone.utc) + timedelta(hours=JWT_EXP_DELTA_HOURS)

    # Формируем полезную нагрузку для токена
    token_payload = {
        "user_id": db_user.id,
        "exp": expiration_time,
        "iat": datetime.datetime.now(timezone.utc)
    }
    # Генерация токена с помощью PyJWT
    token = jwt.encode(token_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    # Формирование ответа с установкой HTTP‑cookie для токена
    response = Response(
        content='{"message": "Login successful!"}',
        media_type="application/json"
    )
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,      # для HTTPS; на локальной разработке можно установить в False
        samesite="None"   # используем "lax" или другой вариант, если не нужны кросс-доменные запросы
    )
    return response

# Функция для получения текущего пользователя по JWT, полученному из cookie
def get_current_user(
    access_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Missing access token")
    try:
        payload = jwt.decode(access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    # Получаем пользователя из БД по идентификатору
    user = crud.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Пример защищённого эндпоинта, к которому можно обратиться только с корректным JWT
@app.get("/protected")
def protected_route(current_user: schemas.UserResponse = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.name}. This is a protected route."}

"""
uvicorn main:app --reload
"""