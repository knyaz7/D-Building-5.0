from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.Config.db import get_session
from src.Controllers.AuthController import AuthController, oauth2_scheme
from src.Controllers.UserMetaController import UserMetaController
from src.Schemas.UserMetaSchemas import UserMetaInput, UserMetaOutput

router = APIRouter(prefix="/api/v1/user_metas", tags=["User metas"])


@router.get("/", response_model=List[UserMetaOutput])
async def get_user_metas(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await UserMetaController.get_all(session)


@router.get("/{task_id}", response_model=UserMetaOutput)
async def get_user_meta(tool_id: int, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await UserMetaController.get_one(tool_id, session)


@router.post("/", response_model=UserMetaOutput)
async def create_user_meta(tool_id: UserMetaInput, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await UserMetaController.create(tool_id, session)


@router.put("/{task_id}", response_model=UserMetaOutput)
async def update_user_meta(tool_id: int, task_data: UserMetaInput, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await UserMetaController.update(tool_id, task_data, session)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_meta(tool_id: int, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await UserMetaController.delete(tool_id, session)
