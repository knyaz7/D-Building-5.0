from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.Controllers.PointController import PointController
from src.Controllers.ToolController import ToolController
from src.Models.Task import Task
from src.Schemas.PointSchemas import PointOutput
from src.Schemas.TaskSchemas import TaskInput, TaskOutput, TaskUpdate
from src.Schemas.CommentSchemas import CommentOutput

from src.Controllers.CommentController import CommentController
from src.Schemas.ToolSchemas import ToolOutput


class TaskController:
    @staticmethod
    async def get_all(session: AsyncSession) -> List[TaskOutput]:
        result = await session.execute(select(Task))
        tasks = result.scalars().all()

        comments: List[CommentOutput] = []
        tools: List[ToolOutput] = []
        points: List[PointOutput] = []
        for task in tasks:
            for comment in task.comments:
                result = await CommentController.get_one(comment, session)
                comments.append(result)
            task.comments = comments
            comments = []
            for tool in task.stack:
                result = await ToolController.get_one(tool, session)
                tools.append(result)
            task.stack = tools
            tools = []
            for point in task.points:
                result = await PointController.get_one(point, session)
                points.append(result)
            task.points = points
            points = []
        return [TaskOutput.from_orm(task) for task in tasks]

    @staticmethod
    async def get_one(task_id: int, session: AsyncSession) -> TaskOutput:
        result = await session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        if task is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        comments: List[CommentOutput] = []
        for comment in task.comments:
            result = await CommentController.get_one(comment, session)
            comments.append(result)
        task.comments = comments

        tools: List[ToolOutput] = []
        for tool in task.stack:
            result = await ToolController.get_one(tool, session)
            tools.append(result)
        task.stack = tools

        points: List[PointOutput] = []
        for point in task.points:
            result = await PointController.get_one(point, session)
            points.append(result)
        task.points = points

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

        comments: List[CommentOutput] = []
        for comment in task.comments:
            result = await CommentController.get_one(comment, session)
            comments.append(result)
        task.comments = comments

        tools: List[ToolOutput] = []
        for tool in task.stack:
            result = await ToolController.get_one(tool, session)
            tools.append(result)
        task.stack = tools

        points: List[PointOutput] = []
        for point in task.points:
            result = await PointController.get_one(point, session)
            points.append(result)
        task.points = points

        return TaskOutput.from_orm(task)

    @staticmethod
    async def delete(task_id: int, session: AsyncSession):
        result = await session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        if task is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        await session.delete(task)
        await session.commit()
