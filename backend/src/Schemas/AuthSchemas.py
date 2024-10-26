from pydantic import BaseModel


class AuthUpdateTokens(BaseModel):
    access_token: str
    refresh_token: str


class AuthRefreshToken(BaseModel):
    refresh_token: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
