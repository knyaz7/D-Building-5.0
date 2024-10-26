from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.Models.MasterTask import MasterTask
from src.Schemas.MasterTaskSchemas import MasterTaskInput, MasterTaskOutput


class MasterTaskController:
    @staticmethod
    async def get_all(session: AsyncSession) -> List[MasterTaskOutput]:
        result = await session.execute(select(MasterTask))
        tasks = result.scalars().all()
        return [MasterTaskOutput.from_orm(task) for task in tasks]

    @staticmethod
    async def get_one(task_id: int, session: AsyncSession) -> MasterTaskOutput:
        result = await session.execute(select(MasterTask).where(MasterTask.id == task_id))
        task = result.scalar_one_or_none()
        if task is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        return MasterTask.from_orm(task)

    @staticmethod
    async def create(task: MasterTaskInput, session: AsyncSession) -> MasterTaskOutput:
        existing_task = await session.execute(
            select(MasterTask).filter(MasterTask.name == task.name)
        )
        if existing_task.scalar() is not None:
            raise HTTPException(status_code=400, detail="Задача с таким названием уже существует.")

        new_task = MasterTask(**task.dict())
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)

        return MasterTaskOutput.from_orm(new_task)

    @staticmethod
    async def update(task_id: int, task_data: MasterTaskInput, session: AsyncSession) -> MasterTaskOutput:
        result = await session.execute(select(MasterTask).where(MasterTask.id == task_id))
        task = result.scalar_one_or_none()
        if task is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        # Обновляем поля пользователя
        for key, value in task_data.dict(exclude_unset=True).items():
            setattr(task, key, value)

        # Сохраняем изменения в базе данных
        session.add(task)
        await session.commit()

        # Сериализация обновленного пользователя
        return MasterTask.from_orm(task)

    @staticmethod
    async def delete(task_id: int, session: AsyncSession):
        result = await session.execute(select(MasterTask).where(MasterTask.id == task_id))
        task = result.scalar_one_or_none()
        if task is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        await session.delete(task)
        await session.commit()
