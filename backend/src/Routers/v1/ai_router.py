from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.Config.db import get_session
from src.Controllers.AuthController import AuthController, oauth2_scheme
from src.Controllers.AiController import AiController
from src.Schemas.UserSchemas import UserOutput
from src.Schemas.AiSchemas import AiInput

router = APIRouter(prefix="/api/v1/ai", tags=["ai"])

@router.post("/", response_model=List[UserOutput])  
async def get_rec_users(ai_data: AiInput, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await AiController.get_rec_users(ai_data, session)
