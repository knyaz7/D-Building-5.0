from typing import List

from fastapi import HTTPException
from sqlalchemy import select, update, literal
from sqlalchemy.ext.asyncio import AsyncSession

from src.Models.Stage import Stage
from src.Schemas.StageSchemas import StageInput, StageOutput, MoveTask
from src.Controllers.TaskController import TaskController
from src.Schemas.TaskSchemas import TaskInput, TaskOutput


class StageController:
    @staticmethod
    async def get_all(session: AsyncSession) -> List[StageOutput]:
        result = await session.execute(select(Stage))
        stages = result.scalars().all()
        tasks: List[TaskOutput] = []
        for stage in stages:
            for task in stage.tasks:
                result = await TaskController.get_one(task, session)
                tasks.append(result)
            stage.tasks = tasks
            tasks = []
        return [StageOutput.from_orm(stage) for stage in stages]

    @staticmethod
    async def get_one(tool_id: int, session: AsyncSession) -> StageOutput:
        result = await session.execute(select(Stage).where(Stage.id == tool_id))
        stage = result.scalar_one_or_none()
        if stage is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        tasks: List[TaskOutput] = []
        for task in stage.tasks:
            result = await TaskController.get_one(task, session)
            tasks.append(result)
        stage.tasks = tasks

        return StageOutput.from_orm(stage)

    @staticmethod
    async def create(tool: StageInput, session: AsyncSession) -> StageOutput:
        existing_tool = await session.execute(
            select(Stage).filter(Stage.name == tool.name)
        )
        if existing_tool.scalar() is not None:
            raise HTTPException(status_code=400, detail="Инструмент с таким названием уже существует.")

        new_tool = Stage(**tool.dict())
        session.add(new_tool)
        await session.commit()
        await session.refresh(new_tool)

        return StageOutput.from_orm(new_tool)

    @staticmethod
    async def update(tool_id: int, tool_data: StageInput, session: AsyncSession) -> StageOutput:
        result = await session.execute(select(Stage).where(Stage.id == tool_id))
        stage = result.scalar_one_or_none()
        if stage is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        # Обновляем поля пользователя
        for key, value in tool_data.dict(exclude_unset=True).items():
            setattr(stage, key, value)

        tasks: List[TaskOutput] = []
        for task in stage.tasks:
            result = await TaskController.get_one(task, session)
            tasks.append(result)
        stage.tasks = tasks

        # Сохраняем изменения в базе данных
        session.add(stage)
        await session.commit()

        # Сериализация обновленного пользователя
        return StageOutput.from_orm(stage)

    @staticmethod
    async def create_task(stage_id: int, task_data: TaskInput, session: AsyncSession) -> TaskOutput:
        task = await TaskController.create(task_data, session)
        result = await session.execute(
            select(Stage).where(Stage.id == stage_id)
        )
        stage = result.scalar_one_or_none()
        if stage is None:
            raise HTTPException(400, "Bad request")

        await session.execute(
            update(Stage)
            .where(Stage.id == stage_id)
            .values(tasks=literal(task.id).concat(Stage.tasks))  # Используйте append для добавления нового id в список
        )

        await session.commit()
        return TaskOutput.from_orm(task)

    @staticmethod
    async def delete_task(stage_id: int, task_id: int, session: AsyncSession):
        await TaskController.delete(task_id, session)
        result = await session.execute(
            select(Stage).where(Stage.id == stage_id)
        )
        stage = result.scalar_one_or_none()
        if stage is None:
            raise HTTPException(400, "Bad request")

        # Убираем comment_id из списка комментариев
        current_tasks = stage.tasks or []
        updated_tasks = [cid for cid in current_tasks if cid != task_id]

        # Обновляем задачу с новым списком комментариев
        await session.execute(
            update(Stage)
            .where(Stage.id == stage_id)
            .values(tasks=updated_tasks)
        )

        await session.commit()

    @staticmethod
    async def move_task(task_id, move: MoveTask, session: AsyncSession):
        from_stage_result = await session.execute(
            select(Stage).where(Stage.id == move.from_stage_id)
        )
        from_stage = from_stage_result.scalar_one_or_none()
        if from_stage is None:
            raise HTTPException(400, "Bad request")

        to_stage_result = await session.execute(
            select(Stage).where(Stage.id == move.to_stage_id)
        )
        to_stage = to_stage_result.scalar_one_or_none()
        if to_stage is None:
            raise HTTPException(400, "Bad request")

        await session.execute(
            update(Stage)
            .where(Stage.id == to_stage.id)
            .values(tasks=literal(task_id).concat(Stage.tasks))
        )

        current_tasks = from_stage.tasks or []
        updated_tasks = [cid for cid in current_tasks if cid != task_id]

        # Обновляем задачу с новым списком комментариев
        await session.execute(
            update(Stage)
            .where(Stage.id == from_stage.id)
            .values(tasks=updated_tasks)
        )

        await session.commit()
