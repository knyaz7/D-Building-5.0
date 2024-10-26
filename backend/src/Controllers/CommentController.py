from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.Models.Comment import Comment
from src.Schemas.CommentSchemas import CommentInput, CommentOutput
from src.Models.Task import Task


class CommentController:
    @staticmethod
    async def get_one(comment_id: int, session: AsyncSession) -> CommentOutput:
        result = await session.execute(select(Task).where(Comment.id == comment_id))
        comment = result.scalar_one_or_none()
        if comment is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        return CommentOutput.from_orm(comment)

    @staticmethod
    async def create(comment: CommentInput, session: AsyncSession) -> CommentOutput:
        new_comment = Comment(**comment.dict())
        session.add(new_comment)
        await session.commit()
        await session.refresh(new_comment)

        return CommentOutput.from_orm(new_comment)

    @staticmethod
    async def update(comment_id: int, comment_data: CommentInput, session: AsyncSession) -> CommentOutput:
        result = await session.execute(select(Comment).where(Comment.id == comment_id))
        comment = result.scalar_one_or_none()
        if comment is None:
            raise HTTPException(status_code=404, detail="Комментарий не найден")

        for key, value in comment_data.dict(exclude_unset=True).items():
            setattr(comment, key, value)

        # Сохраняем изменения в базе данных
        session.add(comment)
        await session.commit()

        return CommentOutput.from_orm(comment)

    @staticmethod
    async def delete(comment_id: int, session: AsyncSession):
        result = await session.execute(select(Comment).where(Comment.id == comment_id))
        comment = result.scalar_one_or_none()
        if comment is None:
            raise HTTPException(status_code=404, detail="Комментарий не найден")

        await session.delete(comment)
        await session.commit()
