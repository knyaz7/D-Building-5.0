from typing import Optional, List

from pydantic import BaseModel


class TaskInput(BaseModel):
    user_id: int
    title: str
    description: str
    stack: Optional[List[int]] = None


class TaskUpdate(BaseModel):
    title: str
    description: str
    stack: List[int]
    position: int
    points: List[int]
    comments: List[int]

    class Config:
        orm_mode = True
        from_attributes = True


class TaskOutput(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    stack: List[int]
    position: int
    points: List[int]
    comments: List[int]

    class Config:
        orm_mode = True
        from_attributes = True
