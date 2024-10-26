from pydantic import BaseModel


class CommentInput(BaseModel):
    text: str
    user_id: int


class CommentOutput(BaseModel):
    id: int
    text: str
    user_id: int

    class Config:
        orm_mode = True
