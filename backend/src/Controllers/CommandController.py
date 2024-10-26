from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.Models.Command import Command
from src.Schemas.CommandSchemas import CommandInput, CommandOutput


class CommandController:
    @staticmethod
    async def get_all(session: AsyncSession) -> List[CommandOutput]:
        result = await session.execute(select(Command))
        commands = result.scalars().all()
        return [CommandOutput.from_orm(command) for command in commands]

    @staticmethod
    async def get_one(command_id: int, session: AsyncSession) -> CommandOutput:
        result = await session.execute(select(Command).where(Command.id == command_id))
        command = result.scalar_one_or_none()
        if command is None:
            raise HTTPException(status_code=404, detail="Команда не найдена")
        return CommandOutput.from_orm(command)
    
    @staticmethod
    async def create(command: CommandInput, session: AsyncSession) -> CommandOutput:
        query = await session.execute(
            select(Command).where(Command.name == command.name)
        )
        result = query.scalar_one_or_none()
        if result is not None:
            raise HTTPException(409, f"Команда '{command.name}' уже существует")

        new_command = Command(**command.dict())
        session.add(new_command)
        await session.commit()

        return new_command

    @staticmethod
    async def update(command_id: int, command_data: CommandInput, session: AsyncSession) -> CommandOutput:
        result = await session.execute(select(Command).where(Command.id == command_id))
        command = result.scalar_one_or_none()
        if command is None:
            raise HTTPException(status_code=404, detail="Команда не найдена")

        # Обновляем поля пользователя
        for key, value in command_data.dict(exclude_unset=True).items():
            setattr(command, key, value)

        # Сохраняем изменения в базе данных
        session.add(command)
        await session.commit()

        # Сериализация обновленного пользователя
        return CommandOutput.from_orm(command)

    @staticmethod
    async def delete(command_id: int, session: AsyncSession):
        result = await session.execute(select(Command).where(Command.id == command_id))
        command = result.scalar_one_or_none()
        if command is None:
            raise HTTPException(status_code=404, detail="Команда не найдена")

        await session.delete(command)
        await session.commit()
