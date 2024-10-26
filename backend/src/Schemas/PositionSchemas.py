from pydantic import BaseModel


class PositionInput(BaseModel):
    name: str


class PositionOutput(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
