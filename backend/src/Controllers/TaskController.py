from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.Models.Task import Task
from src.Schemas.TaskSchemas import TaskInput, TaskOutput, TaskUpdate


class TaskController:
    @staticmethod
    async def get_all(session: AsyncSession) -> List[TaskOutput]:
        result = await session.execute(select(Task))
        tasks = result.scalars().all()
        return [TaskOutput.from_orm(task) for task in tasks]

    @staticmethod
    async def get_one(task_id: int, session: AsyncSession) -> TaskOutput:
        result = await session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        if task is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        return TaskOutput.from_orm(task)

    @staticmethod
    async def create(task: TaskInput, session: AsyncSession) -> TaskOutput:
        existing_task = await session.execute(
            select(Task).filter(Task.title == task.title)
        )
        if existing_task.scalar() is not None:
            raise HTTPException(status_code=400, detail="Задача с таким названием уже существует.")

        new_task = await Task.create(session, **task.dict())
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)

        return TaskOutput.from_orm(new_task)

    @staticmethod
    async def update(task_id: int, task_data: TaskUpdate, session: AsyncSession) -> TaskOutput:
        result = await session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        if task is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        # Обновляем поля пользователя
        for key, value in task_data.dict(exclude_unset=True).items():
            setattr(task, key, value)

        # Сохраняем изменения в базе данных
        session.add(task)
        await session.commit()

        # Сериализация обновленного пользователя
        return TaskOutput.from_orm(task)

    @staticmethod
    async def delete(task_id: int, session: AsyncSession):
        result = await session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        if task is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        await session.delete(task)
        await session.commit()
