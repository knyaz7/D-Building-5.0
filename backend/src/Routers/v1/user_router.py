import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.Config.db import get_session
from src.Controllers.UserController import UserController
from src.Schemas.UserSchemas import UserInput, UserOutput, UserOutputTokens

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("/", response_model=List[UserOutput])
async def get_users(session: AsyncSession = Depends(get_session)):
    return await UserController.get_users(session)


@router.post("/", response_model=UserOutputTokens)
async def create_user(user: UserInput, session: AsyncSession = Depends(get_session)):
    return await UserController.create_user(user, session)
