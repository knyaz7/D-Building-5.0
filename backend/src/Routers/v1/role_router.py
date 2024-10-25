from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.Config.db import get_session
from src.Controllers.RoleController import RoleController
from src.Schemas.RoleSchemas import RoleInput, RoleOutput

router = APIRouter(prefix="/api/v1/roles", tags=["Roles"])


@router.post("", response_model=RoleOutput)
async def create_user(role: RoleInput, session: AsyncSession = Depends(get_session)):
    return await RoleController.create_role(role, session)
