import time
from sqlalchemy.orm import Session
from models import User

# in-memory кэш для пользователей
user_cache = {}
CACHE_TTL = 60  # время жизни кэша в секундах

def get_user_by_email(db: Session, email: str):
    current_time = time.time()
    # Если пользователь уже в кэше и данные актуальны, возвращаем их
    if email in user_cache:
        cached_time, cached_user = user_cache[email]
        if current_time - cached_time < CACHE_TTL:
            return cached_user
        else:
            # Если время кэша истекло, удаляем запись
            del user_cache[email]
    # Если данных в кэше нет или они устарели, запрашиваем пользователя из БД
    user = db.query(User).filter(User.email == email).first()
    if user:
        user_cache[email] = (current_time, user)
    return user
