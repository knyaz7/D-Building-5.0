from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.Config.db import get_session
from src.Controllers.CommandController import CommandController
from src.Schemas.CommandSchemas import CommandInput, CommandOutput

router = APIRouter(prefix="/api/v1/commands", tags=["Commands"])


@router.get("/", response_model=List[CommandOutput])
async def get_commands(session: AsyncSession = Depends(get_session)):
    return await CommandController.get_all(session)


@router.get("/{command_id}", response_model=CommandOutput)
async def get_command(command_id: int, session: AsyncSession = Depends(get_session)):
    return await CommandController.get_one(command_id, session)

@router.post("/", response_model=CommandOutput)
async def create_command(command: CommandInput, session: AsyncSession = Depends(get_session)):
    return await CommandController.create_command(command, session)


@router.put("/{command_id}", response_model=CommandOutput)
async def update_command(command_id: int, command_data: CommandInput, session: AsyncSession = Depends(get_session)):
    return await CommandController.update(command_id, command_data, session)


@router.delete("/{command_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_command(command_id: int, session: AsyncSession = Depends(get_session)):
    return await CommandController.delete(command_id, session)