from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'users'

    id_users = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    second_name = Column(String, index=True)
    education = Column(String)
    living_country = Column(String)
    living_city = Column(String)
    about = Column(String)
    # По умолчанию поставим нули
    count_proj = Column(Integer, default=0)
    has_invested = Column(Integer)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    telegram = Column(String)
