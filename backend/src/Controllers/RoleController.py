from typing import List
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.Models.Role import Role
from src.Schemas.RoleSchemas import RoleInput, RoleOutput


class RoleController:
    @staticmethod
    async def create(role: RoleInput, session: AsyncSession) -> RoleOutput:
        query = await session.execute(
            select(Role).where(Role.name == role.name)
        )
        result = query.scalar_one_or_none()
        if result is not None:
            raise HTTPException(409, f"Роль '{role.name}' уже существует")

        new_role = Role(**role.dict())
        session.add(new_role)
        await session.commit()

        return new_role
    
    @staticmethod
    async def get_all(session: AsyncSession) -> List[RoleOutput]:
        result = await session.execute(select(Role))
        roles = result.scalars().all()
        return [RoleOutput.from_orm(role) for role in roles]

    @staticmethod
    async def get_one(role_id: int, session: AsyncSession) -> RoleOutput:
        result = await session.execute(select(Role).where(Role.id == role_id))
        role = result.scalar_one_or_none()
        if role is None:
            raise HTTPException(status_code=404, detail="Роль не найдена")
        return RoleOutput.from_orm(role)
