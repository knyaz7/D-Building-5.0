from typing import List

from fastapi import HTTPException
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.Models.Role import Role
from src.Models.User import User
from src.Schemas.UserSchemas import UserInput, UserOutput, UserOutputTokens
from src.Controllers.AuthController import AuthController


class UserController:
    @staticmethod
    async def get_all(session: AsyncSession) -> List[UserOutput]:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return [UserOutput.from_orm(user) for user in users]

    @staticmethod
    async def get_one(user_id: int, session: AsyncSession) -> UserOutput:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return UserOutput.from_orm(user)

    @staticmethod
    async def create(user: UserInput, session: AsyncSession) -> UserOutputTokens:
        existing_user = await session.execute(
            select(User).filter(or_(User.username == user.username, User.fullname == user.fullname))
        )
        if existing_user.scalar() is not None:
            raise HTTPException(status_code=400, detail="Fullname or username already registered")

        hashed_password = AuthController.hash_password(user.password)

        new_user = User(
            username=user.username,
            fullname=user.fullname,
            password_hash=hashed_password
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        # Генерация токенов с использованием id и username
        access_token = AuthController.create_access_token(user_id=new_user.id, username=new_user.username)
        refresh_token = AuthController.create_refresh_token(user_id=new_user.id, username=new_user.username)

        return UserOutputTokens(
            id=new_user.id,
            username=new_user.username,
            fullname=new_user.fullname,
            password_hash=new_user.password_hash,
            access_key=access_token,
            refresh_token=refresh_token,
            token_type="Bearer"
        )

    @staticmethod
    async def update(user_id: int, user_data: UserInput, session: AsyncSession) -> UserOutput:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        # Обновляем поля пользователя
        for key, value in user_data.dict(exclude_unset=True).items():
            setattr(user, key, value)

        # Сохраняем изменения в базе данных
        session.add(user)
        await session.commit()

        # Сериализация обновленного пользователя
        return UserOutput.from_orm(user)

    @staticmethod
    async def delete(user_id: int, session: AsyncSession):
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        await session.delete(user)
        await session.commit()
