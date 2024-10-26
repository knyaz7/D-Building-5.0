from pydantic import BaseModel


class ToolInput(BaseModel):
    name: str


class ToolOutput(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
