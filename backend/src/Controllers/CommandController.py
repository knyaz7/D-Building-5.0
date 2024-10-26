from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.Models.Command import Command
from src.Schemas.CommandSchemas import CommandInput, CommandOutput


class CommandController:
    @staticmethod
    async def create_command(command: CommandInput, session: AsyncSession) -> CommandOutput:
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
