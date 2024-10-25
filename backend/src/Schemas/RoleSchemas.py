from pydantic import BaseModel


class RoleInput(BaseModel):
    name: str


class RoleOutput(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
