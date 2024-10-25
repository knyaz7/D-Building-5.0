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
    async def get_users(session: AsyncSession) -> List[UserOutput]:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return [UserOutput.from_orm(user) for user in users]

    @staticmethod
    async def create_user(user: UserInput, session: AsyncSession) -> UserOutputTokens:
        existing_user = await session.execute(
            select(User).filter(or_(User.username == user.username, User.fullname == user.fullname))
        )
        if existing_user.scalar() is not None:
            raise HTTPException(status_code=400, detail="Fullname or username already registered")

        existing_role = await session.execute(
            select(Role).filter(Role.id == user.role_id)
        )
        if existing_role.scalar_one_or_none() is None:
            raise HTTPException(status_code=404, detail="Role does not exist")

        hashed_password = AuthController.hash_password(user.password)

        new_user = User(
            username=user.username,
            fullname=user.fullname,
            password_hash=hashed_password,
            role_id=user.role_id
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        # Генерация токенов с использованием id и email
        access_token = AuthController.create_access_token(user_id=new_user.id, username=new_user.username)
        refresh_token = AuthController.create_refresh_token(user_id=new_user.id, username=new_user.username)

        return UserOutputTokens(
            id=new_user.id,
            username=new_user.username,
            fullname=new_user.fullname,
            password_hash=new_user.password_hash,
            role_id=new_user.role_id,
            access_key=access_token,
            refresh_token=refresh_token,
            token_type="Bearer"
        )
