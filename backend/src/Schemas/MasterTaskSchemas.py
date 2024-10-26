from pydantic import BaseModel
from datetime import datetime


class MasterTaskInput(BaseModel):
    tasks: list
    created_at: datetime
    deadline: datetime


class MasterTaskOutput(BaseModel):
    id: int
    tasks: list
    created_at: datetime
    deadline: datetime

    class Config:
        orm_mode = True
