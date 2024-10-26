from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.Config.db import get_session
from src.Controllers.PointController import PointController
from src.Schemas.PointSchemas import PointInput, PointOutput

router = APIRouter(prefix="/api/v1/points", tags=["Points"])


@router.get("/", response_model=List[PointOutput])
async def get_point(session: AsyncSession = Depends(get_session)):
    return await PointController.get_all(session)


@router.get("/{point_id}", response_model=PointOutput)
async def get_point(point_id: int, session: AsyncSession = Depends(get_session)):
    return await PointController.get_one(point_id, session)


@router.post("/", response_model=PointOutput)
async def create_point(point: PointInput, session: AsyncSession = Depends(get_session)):
    return await PointController.create(point, session)


@router.put("/{point_id}", response_model=PointOutput)
async def update_point(point_id: int, point_data: PointInput, session: AsyncSession = Depends(get_session)):
    return await PointController.update(point_id, point_data, session)


@router.delete("/{point_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_point(point_id: int, session: AsyncSession = Depends(get_session)):
    return await PointController.delete(point_id, session)
