import hashlib
import os
import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session

API_URL = "http://46.38.47.190/register"
API_KEY = ("2d0e567e130dbdd482696d3b32dca182d588c436761f42d1e413f86c81bdcf42"
           "5a842b9db7fb90250ad72ba6e79375f7ca19ffc516ace800ae37b581b92b416c")

DB_URL = os.environ["DATABASE_URL"]

payload = {
    "name": "Didi",
    "second_name": "Pi",
    "email": "losck@bang.com",
    "password": "dudeNude123",
}

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    second_name = Column(String(50))
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    @staticmethod
    def hash_pwd(raw: str) -> str:
        return hashlib.sha256(raw.encode()).hexdigest()

    @classmethod
    def from_payload(cls, d: dict) -> "User":
        return cls(
            name=d["name"],
            second_name=d.get("second_name"),
            email=d["email"],
            password_hash=cls.hash_pwd(d["password"]),
        )

engine = create_engine(DB_URL, echo=False, future=True)
Base.metadata.create_all(engine)

headers = {"Content-Type": "application/json", "API-Key": API_KEY}
resp = requests.post(API_URL, json=payload, headers=headers, timeout=10)

if resp.ok:
    print("✅  API ответ:", resp.json())

    with Session(engine) as session:
        if session.query(User).filter_by(email=payload["email"]).first():
            print("ℹ️  Пользователь уже есть в БД")
        else:
            session.add(User.from_payload(payload))
            session.commit()
            print("✅  Пользователь сохранён в БД")
else:
    print("❌  Ошибка API:", resp.status_code, resp.text)
