from pydantic import BaseModel


class PointInput(BaseModel):
    text: str
    status: bool


class PointOutput(BaseModel):
    id: int
    text: str
    status: bool

    class Config:
        orm_mode = True
