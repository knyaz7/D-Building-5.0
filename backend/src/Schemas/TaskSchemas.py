from typing import Optional, List

from pydantic import BaseModel

from src.Schemas.CommentSchemas import CommentOutput


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
    comments: List[CommentOutput]

    class Config:
        orm_mode = True
        from_attributes = True
