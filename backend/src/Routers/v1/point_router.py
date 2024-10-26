from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.Config.db import get_session
from src.Controllers.AuthController import AuthController, oauth2_scheme
from src.Controllers.PointController import PointController
from src.Schemas.PointSchemas import PointInput, PointOutput

router = APIRouter(prefix="/api/v1/points", tags=["Points"])


@router.get("/", response_model=List[PointOutput])
async def get_point(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await PointController.get_all(session)


@router.get("/{point_id}", response_model=PointOutput)
async def get_point(point_id: int, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await PointController.get_one(point_id, session)


@router.post("/", response_model=PointOutput)
async def create_point(point: PointInput, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await PointController.create(point, session)


@router.put("/{point_id}", response_model=PointOutput)
async def update_point(point_id: int, point_data: PointInput, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await PointController.update(point_id, point_data, session)


@router.delete("/{point_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_point(point_id: int, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await PointController.delete(point_id, session)
