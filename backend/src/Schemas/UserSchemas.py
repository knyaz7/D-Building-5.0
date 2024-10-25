from pydantic import BaseModel
from typing import Optional


class UserInput(BaseModel):
    username: str
    fullname: str
    password: str
    role_id: int


class UserOutput(BaseModel):
    id: int
    username: str
    fullname: str
    role_id: int
    rating: Optional[float] = None

    class Config:
        orm_mode = True
        from_attributes = True


class UserOutputTokens(BaseModel):
    id: int
    username: str
    fullname: str
    role_id: int
    rating: Optional[float] = None
    access_key: str
    refresh_token: str
    token_type: str

    class Config:
        orm_mode = True
