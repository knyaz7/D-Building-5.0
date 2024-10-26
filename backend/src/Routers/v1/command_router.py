from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.Config.db import get_session
from src.Controllers.CommandController import CommandController
from src.Schemas.CommandSchemas import CommandInput, CommandOutput

router = APIRouter(prefix="/api/v1/commands", tags=["Command"])


@router.post("/", response_model=CommandOutput)
async def create_command(command: CommandInput, session: AsyncSession = Depends(get_session)):
    return await CommandController.create_command(command, session)
