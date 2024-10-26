from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.Models.Point import Point
from src.Schemas.PointSchemas import PointInput, PointOutput


class PointController:
    @staticmethod
    async def get_all(session: AsyncSession) -> List[PointOutput]:
        result = await session.execute(select(Point))
        points = result.scalars().all()
        return [PointOutput.from_orm(point) for point in points]

    @staticmethod
    async def get_one(point_id: int, session: AsyncSession) -> PointOutput:
        result = await session.execute(select(Point).where(Point.id == point_id))
        point = result.scalar_one_or_none()
        if point is None:
            raise HTTPException(status_code=404, detail="Пункт не найден")
        return PointOutput.from_orm(point)

    @staticmethod
    async def create(point: PointInput, session: AsyncSession) -> PointOutput:
        existing_point = await session.execute(
            select(Point).filter(Point.text == point.text)
        )
        if existing_point.scalar() is not None:
            raise HTTPException(status_code=400, detail="Пункт с таким названием уже существует.")

        new_point = Point(**point.dict())
        session.add(new_point)
        await session.commit()
        await session.refresh(new_point)

        return PointOutput.from_orm(new_point)

    @staticmethod
    async def update(point_id: int, point_data: PointInput, session: AsyncSession) -> PointOutput:
        result = await session.execute(select(Point).where(Point.id == point_id))
        point = result.scalar_one_or_none()
        if point is None:
            raise HTTPException(status_code=404, detail="Пункт не найден")

        # Обновляем поля пользователя
        for key, value in point_data.dict(exclude_unset=True).items():
            setattr(point, key, value)

        # Сохраняем изменения в базе данных
        session.add(point)
        await session.commit()

        # Сериализация обновленного пользователя
        return PointOutput.from_orm(point)

    @staticmethod
    async def delete(point_id: int, session: AsyncSession):
        result = await session.execute(select(Point).where(Point.id == point_id))
        point = result.scalar_one_or_none()
        if point is None:
            raise HTTPException(status_code=404, detail="Пункт не найден")

        await session.delete(point)
        await session.commit()
