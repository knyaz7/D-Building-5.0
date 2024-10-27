from typing import List

from fastapi import HTTPException
from sqlalchemy import select, update, literal, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.Controllers.TaskController import TaskController
from src.Models.MasterTask import MasterTask
from src.Models.Stage import Stage
from src.Models.Task import Task
from src.Models.User import User
from src.Schemas.MasterTaskSchemas import MasterTaskInput, MasterTaskOutput
from src.Schemas.TaskSchemas import TaskOutput, TaskInput


class MasterTaskController:
    @staticmethod
    async def get_all(session: AsyncSession) -> List[MasterTaskOutput]:
        result = await session.execute(select(MasterTask))
        master_tasks = result.scalars().all()
        tasks: List[TaskOutput] = []
        for master_task in master_tasks:
            for task in master_task.tasks:
                result = await TaskController.get_one(task, session)
                tasks.append(result)
            master_task.tasks = tasks
            tasks = []
        return [MasterTaskOutput.from_orm(master_task) for master_task in master_tasks]

    @staticmethod
    async def get_one(task_id: int, session: AsyncSession) -> MasterTaskOutput:
        result = await session.execute(select(MasterTask).where(MasterTask.id == task_id))
        master_task = result.scalar_one_or_none()
        if master_task is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        tasks: List[TaskOutput] = []
        for task in master_task.tasks:
            result = await TaskController.get_one(task, session)
            tasks.append(result)
        master_task.tasks = tasks

        return MasterTaskOutput.from_orm(master_task)

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
        master_task = result.scalar_one_or_none()
        if master_task is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        # Обновляем поля пользователя
        for key, value in task_data.dict(exclude_unset=True).items():
            setattr(master_task, key, value)

        # Сохраняем изменения в базе данных
        session.add(master_task)
        await session.commit()

        tasks: List[TaskOutput] = []
        for task in master_task.tasks:
            result = await TaskController.get_one(task, session)
            tasks.append(result)
        master_task.tasks = tasks

        # Сериализация обновленного пользователя
        return MasterTaskOutput.from_orm(master_task)

    @staticmethod
    async def delete(task_id: int, session: AsyncSession):
        result = await session.execute(select(MasterTask).where(MasterTask.id == task_id))
        task = result.scalar_one_or_none()
        if task is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        await session.delete(task)
        await session.commit()

    @staticmethod
    async def create_task(master_task_id: int, task_data: TaskInput, session: AsyncSession) -> TaskOutput:
        user_stmt = await session.execute(
            select(User).where(User.id == task_data.user_id)
        )
        user = user_stmt.scalar_one_or_none()
        if user is None:
            raise HTTPException(404, "AAAAAAAAAAAa")

        task = await TaskController.create(task_data, session)
        result = await session.execute(
            select(MasterTask).where(MasterTask.id == master_task_id)
        )
        master_task = result.scalar_one_or_none()
        if master_task is None:
            raise HTTPException(400, "AAAAAAAAAAAa")

        await session.execute(
            update(MasterTask)
            .where(MasterTask.id == master_task_id)
            .values(tasks=literal(task.id).concat(MasterTask.tasks))
        )

        to_stage_result = await session.execute(
            select(Stage).where(Stage.id == 1)
        )
        to_stage = to_stage_result.scalar_one_or_none()
        if to_stage is None:
            raise HTTPException(400, "AAAAAAAAAAAa")

        await session.execute(
            update(Stage)
            .where(Stage.id == to_stage.id)
            .values(tasks=literal(task.id).concat(Stage.tasks))
        )

        await session.commit()
        return TaskOutput.from_orm(task)

    @staticmethod
    async def delete_task(master_task_id: int, task_id: int, session: AsyncSession):
        await TaskController.delete(task_id, session)
        result = await session.execute(
            select(MasterTask).where(MasterTask.id == master_task_id)
        )
        master_task = result.scalar_one_or_none()
        if master_task is None:
            raise HTTPException(400, "AAAAAAAAAAAa")

        # Убираем comment_id из списка комментариев
        current_tasks = master_task.tasks or []
        updated_tasks = [cid for cid in current_tasks if cid != task_id]

        # Обновляем задачу с новым списком комментариев
        await session.execute(
            update(MasterTask)
            .where(MasterTask.id == master_task_id)
            .values(tasks=updated_tasks)
        )

        from_stage_result = await session.execute(
            select(Stage).where(Stage.tasks.any(task_id))
        )
        from_stage = from_stage_result.scalar_one_or_none()
        if from_stage is None:
            raise HTTPException(400, "AAAAAAAAAAAa")

        current_tasks = from_stage.tasks or []
        updated_tasks = [cid for cid in current_tasks if cid != task_id]

        # Обновляем задачу с новым списком комментариев
        await session.execute(
            update(Stage)
            .where(Stage.id == from_stage.id)
            .values(tasks=updated_tasks)
        )

        await session.commit()
