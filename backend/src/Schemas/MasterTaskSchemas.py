from pydantic import BaseModel
from datetime import datetime


class MasterTaskInput(BaseModel):
    name: str
    deadline: datetime


class MasterTaskOutput(BaseModel):
    id: int
    name: str
    tasks: list
    created_at: datetime
    deadline: datetime

    class Config:
        orm_mode = True
        from_attributes = True
