from pydantic import BaseModel

class UserCreate(BaseModel):
    # name: str
    # second_name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id_users: int
    name: str
    second_name: str
    email: str

    class Config:
        orm_mode = True
