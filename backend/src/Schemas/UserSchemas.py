from pydantic import BaseModel


class UserInput(BaseModel):
    username: str
    fullname: str
    password: str


class UserInputUpdate(BaseModel):
    username: str
    fullname: str
    role_id: int


class UserOutput(BaseModel):
    id: int
    username: str
    fullname: str

    class Config:
        orm_mode = True
        from_attributes = True


class UserOutputTokens(BaseModel):
    id: int
    username: str
    fullname: str
    access_key: str
    refresh_token: str
    token_type: str

    class Config:
        orm_mode = True
