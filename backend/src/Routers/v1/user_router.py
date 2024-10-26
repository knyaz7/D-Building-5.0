from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.Config.db import get_session
from src.Controllers.UserController import UserController
from src.Schemas.UserSchemas import UserInput, UserOutput, UserOutputTokens

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("/", response_model=List[UserOutput])
async def get_users(session: AsyncSession = Depends(get_session)):
    return await UserController.get_all(session)


@router.get("/{user_id}", response_model=UserOutput)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    return await UserController.get_one(user_id, session)


@router.post("/", response_model=UserOutputTokens)
async def create_user(user: UserInput, session: AsyncSession = Depends(get_session)):
    return await UserController.create(user, session)


@router.put("/{user_id}", response_model=UserOutput)
async def update_user(user_id: int, user_data: UserInput, session: AsyncSession = Depends(get_session)):
    return await UserController.update(user_id, user_data, session)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    return await UserController.delete(user_id, session)
