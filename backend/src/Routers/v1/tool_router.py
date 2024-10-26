from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.Config.db import get_session
from src.Controllers.AuthController import AuthController, oauth2_scheme
from src.Controllers.ToolController import ToolController
from src.Schemas.ToolSchemas import ToolInput, ToolOutput

router = APIRouter(prefix="/api/v1/tools", tags=["Tools"])


@router.get("/", response_model=List[ToolOutput])
async def get_tools(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await ToolController.get_all(session)


@router.get("/{task_id}", response_model=ToolOutput)
async def get_tool(tool_id: int, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await ToolController.get_one(tool_id, session)


@router.post("/", response_model=ToolOutput)
async def create_tool(tool_id: ToolInput, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await ToolController.create(tool_id, session)


@router.put("/{task_id}", response_model=ToolOutput)
async def update_tool(tool_id: int, task_data: ToolInput, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await ToolController.update(tool_id, task_data, session)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tool(tool_id: int, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await ToolController.delete(tool_id, session)
