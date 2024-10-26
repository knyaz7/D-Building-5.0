from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.Models.Tool import Tool
from src.Schemas.ToolSchemas import ToolInput, ToolOutput


class ToolController:
    @staticmethod
    async def get_all(session: AsyncSession) -> List[ToolOutput]:
        result = await session.execute(select(Tool))
        tools = result.scalars().all()
        return [ToolOutput.from_orm(tool) for tool in tools]

    @staticmethod
    async def get_one(tool_id: int, session: AsyncSession) -> ToolOutput:
        result = await session.execute(select(Tool).where(Tool.id == tool_id))
        tool = result.scalar_one_or_none()
        if tool is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        return ToolOutput.from_orm(tool)

    @staticmethod
    async def create(tool: ToolInput, session: AsyncSession) -> ToolOutput:
        existing_tool = await session.execute(
            select(Tool).filter(Tool.name == tool.name)
        )
        if existing_tool.scalar() is not None:
            raise HTTPException(status_code=400, detail="Инструмент с таким названием уже существует.")

        new_tool = Tool(**tool.dict())
        session.add(new_tool)
        await session.commit()
        await session.refresh(new_tool)

        return ToolOutput.from_orm(new_tool)

    @staticmethod
    async def update(tool_id: int, tool_data: ToolInput, session: AsyncSession) -> ToolOutput:
        result = await session.execute(select(Tool).where(Tool.id == tool_id))
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
        return ToolOutput.from_orm(tool)

    @staticmethod
    async def delete(tool_id: int, session: AsyncSession):
        result = await session.execute(select(Tool).where(Tool.id == tool_id))
        tool = result.scalar_one_or_none()
        if tool is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        await session.delete(tool)
        await session.commit()
