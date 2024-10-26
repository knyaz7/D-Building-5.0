from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.Models.Position import Position
from src.Schemas.PositionSchemas import PositionInput, PositionOutput


class PositionController:
    @staticmethod
    async def get_all(session: AsyncSession) -> List[PositionOutput]:
        result = await session.execute(select(Position))
        positions = result.scalars().all()
        return [PositionOutput.from_orm(position) for position in positions]

    @staticmethod
    async def get_one(position_id: int, session: AsyncSession) -> PositionOutput:
        result = await session.execute(select(Position).where(Position.id == position_id))
        position = result.scalar_one_or_none()
        if position is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        return PositionOutput.from_orm(position)

    @staticmethod
    async def create(position: PositionInput, session: AsyncSession) -> PositionOutput:
        existing_position = await session.execute(
            select(Position).filter(Position.name == position.name)
        )
        if existing_position.scalar() is not None:
            raise HTTPException(status_code=400, detail="Инструмент с таким названием уже существует.")

        new_position = Position(**position.dict())
        session.add(new_position)
        await session.commit()
        await session.refresh(new_position)

        return PositionOutput.from_orm(new_position)

    @staticmethod
    async def update(position_id: int, tool_data: PositionInput, session: AsyncSession) -> PositionOutput:
        result = await session.execute(select(Position).where(Position.id == position_id))
        position = result.scalar_one_or_none()
        if position is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        # Обновляем поля пользователя
        for key, value in tool_data.dict(exclude_unset=True).items():
            setattr(position, key, value)

        # Сохраняем изменения в базе данных
        session.add(position)
        await session.commit()

        # Сериализация обновленного пользователя
        return PositionOutput.from_orm(position)

    @staticmethod
    async def delete(position_id: int, session: AsyncSession):
        result = await session.execute(select(Position).where(Position.id == position_id))
        position = result.scalar_one_or_none()
        if position is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        await session.delete(position)
        await session.commit()
