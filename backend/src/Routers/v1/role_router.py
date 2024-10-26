from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.Config.db import get_session
from src.Controllers.RoleController import RoleController
from src.Schemas.RoleSchemas import RoleInput, RoleOutput

router = APIRouter(prefix="/api/v1/roles", tags=["Roles"])


# @router.post("/", response_model=RoleOutput)
# async def create_role(role: RoleInput, session: AsyncSession = Depends(get_session)):
#     return await RoleController.create_role(role, session)


@router.get("/", response_model=List[RoleOutput])
async def get_roles(session: AsyncSession = Depends(get_session)):
    return await RoleController.get_all(session)


@router.get("/{role_id}", response_model=RoleOutput)
async def get_role(role_id: int, session: AsyncSession = Depends(get_session)):
    return await RoleController.get_one(role_id, session)