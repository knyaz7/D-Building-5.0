import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.Config.db import get_session
from src.Controllers.UserController import UserController
from src.Schemas.UserSchemas import UserInput, UserOutput

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.post("", response_model=UserOutput)
async def create_user(user: UserInput, session: AsyncSession = Depends(get_session)):
    return await UserController.create_user(user, session)
