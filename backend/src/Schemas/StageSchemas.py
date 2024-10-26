from typing import List

from pydantic import BaseModel
from src.Schemas.TaskSchemas import TaskOutput


class StageInput(BaseModel):
    name: str


class StageOutput(BaseModel):
    id: int
    name: str
    tasks: List[TaskOutput]

    class Config:
        orm_mode = True
        from_attributes = True
