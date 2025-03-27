from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()  # Загрузка переменных окружения (пизды дам за пуш .env)

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Создание подключения к базе данных
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание базового класса для моделей
Base = declarative_base()
