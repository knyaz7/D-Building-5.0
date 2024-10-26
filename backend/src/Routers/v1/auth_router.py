from typing import List, Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.Config.db import get_session
from src.Controllers.AuthController import AuthController
from src.Schemas.AuthSchemas import AuthResponse, AuthRefreshToken, AuthUpdateTokens

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.post("/login/", response_model=AuthResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: AsyncSession = Depends(get_session)):
    return await AuthController.login(form_data, session)


@router.post("/token_refresh/", response_model=AuthUpdateTokens)
async def refresh_access_token(refresh_token: AuthRefreshToken, session: AsyncSession = Depends(get_session)):
    return await AuthController.refresh_access_token(refresh_token, session)