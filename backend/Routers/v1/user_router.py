import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Config.db import get_session
from Schemas.User_Schemas import UserOutput

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get('', response_model=List[UserOutput])
async def get_users(session: AsyncSession = Depends(get_session)):
    response = [ UserOutput(
        id=1,
        username="egor",
        password_hash="help me",
        created_at=datetime.datetime.utcnow(),
    )]
    return response
