from pydantic import BaseModel


class CommentInput(BaseModel):
    text: str
    user_id: int

class CommentPatchInput(BaseModel):
    text: str


class CommentOutput(BaseModel):
    id: int
    text: str
    user_id: int

    class Config:
        orm_mode = True
        from_attributes = True
