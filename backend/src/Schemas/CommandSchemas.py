from pydantic import BaseModel


class CommandInput(BaseModel):
    name: str


class CommandOutput(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
