import time
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate

# кэш в памяти для пользователей
ttl = 60
user_cache = {}

CACHE_TTL = ttl

def get_user_by_email(db: Session, email: str):
    current_time = time.time()
    if email in user_cache:
        cached_time, cached_user = user_cache[email]
        if current_time - cached_time < CACHE_TTL:
            return cached_user
        else:
            del user_cache[email]
    user = db.query(User).filter(User.email == email).first()
    if user:
        user_cache[email] = (current_time, user)
    return user

def get_user_by_id(db: Session, user_id: int):
    """
    Retrieve a user by their ID from the database.
    """
    return db.query(User).filter(User.id_users == user_id).first()

def create_user(db: Session, user: UserCreate):
    """
    Create a new user in the database based on the UserCreate schema.
    """
    new_user = User(
        #name=user.name,
        #second_name=user.second_name,
        email=user.email,
        password=user.password
        # потом можно дополнить
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # Кэшировать только что созданного пользователя
    user_cache[new_user.email] = (time.time(), new_user)
    return new_user

def delete_user(db: Session, user_id: int):
    """
    Удалить пользователя по идентификатору из базы данных.
    """
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        user_cache.pop(user.email, None)
    return user