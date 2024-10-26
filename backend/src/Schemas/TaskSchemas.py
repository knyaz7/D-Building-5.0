from pydantic import BaseModel


class TaskInput(BaseModel):
    title: str
    description: str
    stack: list
    user_id: int
    position: int
    points: list


class TaskOutput(BaseModel):
    id: int
    title: str
    description: str
    stack: list
    user_id: int
    position: int
    points: list
    comments: list

    class Config:
        orm_mode = True
        from_attributes = True
