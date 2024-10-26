from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.Models.UserMeta import UserMeta
from src.Schemas.UserMetaSchemas import UserMetaInput, UserMetaOutput


class UserMetaController:
    @staticmethod
    async def get_all(session: AsyncSession) -> List[UserMetaOutput]:
        result = await session.execute(select(UserMeta))
        tools = result.scalars().all()
        return [UserMetaOutput.from_orm(tool) for tool in tools]

    @staticmethod
    async def get_one(meta_id: int, session: AsyncSession) -> UserMetaOutput:
        result = await session.execute(select(UserMeta).where(UserMeta.id == meta_id))
        tool = result.scalar_one_or_none()
        if tool is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        return UserMetaOutput.from_orm(tool)

    @staticmethod
    async def create(tool: UserMetaInput, session: AsyncSession) -> UserMetaOutput:
        existing_tool = await session.execute(
            select(UserMeta).filter(UserMeta.user_id == tool.user_id)
        )
        if existing_tool.scalar() is not None:
            raise HTTPException(status_code=400, detail="Инструмент с таким названием уже существует.")

        new_tool = UserMeta(**tool.dict())
        session.add(new_tool)
        await session.commit()
        await session.refresh(new_tool)

        return UserMetaOutput.from_orm(new_tool)

    @staticmethod
    async def update(tool_id: int, tool_data: UserMetaInput, session: AsyncSession) -> UserMetaOutput:
        result = await session.execute(select(UserMeta).where(UserMeta.id == tool_id))
        tool = result.scalar_one_or_none()
        if tool is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        # Обновляем поля пользователя
        for key, value in tool_data.dict(exclude_unset=True).items():
            setattr(tool, key, value)

        # Сохраняем изменения в базе данных
        session.add(tool)
        await session.commit()

        # Сериализация обновленного пользователя
        return UserMetaOutput.from_orm(tool)

    @staticmethod
    async def delete(tool_id: int, session: AsyncSession):
        result = await session.execute(select(UserMeta).where(UserMeta.id == tool_id))
        tool = result.scalar_one_or_none()
        if tool is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        await session.delete(tool)
        await session.commit()
