from typing import List

from fastapi import HTTPException
from sqlalchemy import select, update, literal
from sqlalchemy.ext.asyncio import AsyncSession

from src.Controllers.PointController import PointController
from src.Controllers.ToolController import ToolController
from src.Models.Task import Task
from src.Models.Tool import Tool
from src.Schemas.PointSchemas import PointOutput, PointInput
from src.Schemas.TaskSchemas import TaskInput, TaskOutput, TaskUpdate
from src.Schemas.CommentSchemas import CommentOutput, CommentInput

from src.Controllers.CommentController import CommentController
from src.Schemas.ToolSchemas import ToolOutput


class TaskController:
    @staticmethod
    async def get_all(session: AsyncSession) -> List[TaskOutput]:
        with session.no_autoflush:
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
        with session.no_autoflush:
            result = await session.execute(select(Task).where(Task.id == task_id))
            task = result.scalar_one_or_none()
            if task is None:
                raise HTTPException(status_code=404, detail="Задача не найдена")

            # Получаем комментарии как идентификаторы
            comments: List[CommentOutput] = []
            for comment_id in task.comments:  # task.comments должен содержать идентификаторы
                result = await CommentController.get_one(comment_id, session)
                comments.append(result)
            task.comments = comments

            # Получаем инструменты
            tools: List[ToolOutput] = []
            for tool_id in task.stack:  # task.stack должен содержать идентификаторы
                result = await ToolController.get_one(tool_id, session)
                tools.append(result)
            task.stack = tools

            # Получаем точки
            points: List[PointOutput] = []
            for point_id in task.points:  # task.points должен содержать идентификаторы
                result = await PointController.get_one(point_id, session)
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
        with session.no_autoflush:
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

    @staticmethod
    async def create_comment(task_id: int, comment_data: CommentInput, session: AsyncSession) -> CommentOutput:
        comment = await CommentController.create(comment_data, session)
        result = await session.execute(
            select(Task).where(Task.id == task_id)
        )
        task = result.scalar_one_or_none()
        if task is None:
            raise HTTPException(400, "AAAAAAAAAAAa")

        await session.execute(
            update(Task)
            .where(Task.id == task_id)
            .values(comments=literal(comment.id).concat(Task.comments))
        )

        await session.commit()
        return CommentOutput.from_orm(comment)

    @staticmethod
    async def create_point(task_id: int, point_data: PointInput, session: AsyncSession) -> PointOutput:
        point = await PointController.create(point_data, session)
        result = await session.execute(
            select(Task).where(Task.id == task_id)
        )
        task = result.scalar_one_or_none()
        if task is None:
            raise HTTPException(400, "AAAAAAAAAAAa")

        await session.execute(
            update(Task)
            .where(Task.id == task_id)
            .values(points=literal(point.id).concat(Task.points))
        )

        await session.commit()
        return PointOutput.from_orm(point)

    @staticmethod
    async def add_tool(task_id: int, tool_id: int, session: AsyncSession) -> ToolOutput:
        tool = await ToolController.get_one(tool_id, session)

        await session.execute(
            update(Task)
            .where(Task.id == task_id)
            .values(stack=literal(tool.id).concat(Task.stack))
        )

        await session.commit()

        return ToolOutput.from_orm(tool)
