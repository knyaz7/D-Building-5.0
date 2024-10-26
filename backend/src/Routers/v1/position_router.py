from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.Config.db import get_session
from src.Controllers.AuthController import AuthController, oauth2_scheme
from src.Controllers.PositionController import PositionController
from src.Schemas.PositionSchemas import PositionInput, PositionOutput

router = APIRouter(prefix="/api/v1/positions", tags=["Positions"])


@router.get("/", response_model=List[PositionOutput])
async def get_positions(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await PositionController.get_all(session)


@router.get("/{position_id}", response_model=PositionOutput)
async def get_tool(position_id: int, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await PositionController.get_one(position_id, session)


@router.post("/", response_model=PositionOutput)
async def create_tool(position: PositionInput, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await PositionController.create(position, session)


@router.put("/{position_id}", response_model=PositionOutput)
async def update_tool(position_id: int, position_data: PositionInput, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await PositionController.update(position_id, position_data, session)


@router.delete("/{position_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tool(position_id: int, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await PositionController.delete(position_id, session)
