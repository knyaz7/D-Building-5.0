from pydantic import BaseModel
from datetime import datetime


class UserMetaInput(BaseModel):
    position_id: int
    stack: list


class UserMetaOutput(BaseModel):
    id: int
    position_id: int
    stack: list
    employed_at: datetime

    class Config:
        orm_mode = True
