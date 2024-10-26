from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.Config.db import get_session
from src.Controllers.CommentController import CommentController
from src.Schemas.CommentSchemas import CommentInput, CommentPatchInput, CommentOutput

router = APIRouter(prefix="/api/v1/comments", tags=["Comments"])

@router.post("/", response_model=CommentOutput)
async def create_comment(comment: CommentInput, session: AsyncSession = Depends(get_session)):
    return await CommentController.create_comment(comment, session)


@router.patch("/{comment_id}", response_model=CommentOutput)
async def update_comment(comment_id: int, comment_data: CommentPatchInput, session: AsyncSession = Depends(get_session)):
    return await CommentController.update(comment_id, comment_data, session)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int, session: AsyncSession = Depends(get_session)):
    return await CommentController.delete(comment_id, session)