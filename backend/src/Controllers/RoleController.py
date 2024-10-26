from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.Models.Role import Role
from src.Schemas.RoleSchemas import RoleInput, RoleOutput


class RoleController:
    @staticmethod
    async def create_role(role: RoleInput, session: AsyncSession) -> RoleOutput:
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
