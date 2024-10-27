import datetime
import jwt
import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.Models.User import User
from src.Schemas.AuthSchemas import AuthResponse, AuthRefreshToken, AuthUpdateTokens

load_dotenv()

# Создаем объект схемы OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/")


class AuthController:
    # Секретный ключ для JWT
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Время жизни access токена
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # Время жизни refresh токена (1 неделя)

    # Контекст для хеширования паролей
    pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

    @staticmethod
    def hash_password(password: str) -> str:
        return AuthController.pwd_context.hash(password)

    @staticmethod
    async def verify_token(token: str, session: AsyncSession, req_role: int = 2) -> dict:
        try:
            payload = jwt.decode(token, AuthController.SECRET_KEY, algorithms=[AuthController.ALGORITHM])
            user_id: int = payload.get("user_id")
            username: str = payload.get("username")

            user_query = await session.execute(
                select(User).filter(and_(User.id == user_id, User.username == username))
            )
            user = user_query.scalar()

            if user is None:
                raise HTTPException(status_code=403, detail="User not found")

            if user.role_id > req_role:
                raise HTTPException(status_code=403, detail="Access denied")

            return {"user_id": user_id, "username": username}
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    @staticmethod
    def create_access_token(user_id: int, username: str, expires_delta: datetime.timedelta = None) -> str:
        to_encode = {"user_id": user_id, "username": username}
        if expires_delta:
            expire = datetime.datetime.now(datetime.UTC) + expires_delta
        else:
            expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
                minutes=AuthController.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, AuthController.SECRET_KEY, algorithm=AuthController.ALGORITHM)

    @staticmethod
    def create_refresh_token(user_id: int, username: str, expires_delta: datetime.timedelta = None) -> str:
        to_encode = {"user_id": user_id, "username": username}
        if expires_delta:
            expire = datetime.datetime.now(datetime.UTC) + expires_delta
        else:
            expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
                minutes=AuthController.REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, AuthController.SECRET_KEY, algorithm=AuthController.ALGORITHM)

    @staticmethod
    async def refresh_access_token(refresh_token: AuthRefreshToken, session: AsyncSession) -> AuthUpdateTokens:
        payload = await AuthController.verify_token(refresh_token.refresh_token, session)
        user_id = payload["user_id"]
        username = payload["username"]

        new_access_token = AuthController.create_access_token(user_id=user_id, username=username)
        new_refresh_token = AuthController.create_refresh_token(user_id=user_id, username=username)

        return AuthUpdateTokens(
            access_token=new_access_token,
            refresh_token=new_refresh_token
        )

    @staticmethod
    async def login(form_data: OAuth2PasswordRequestForm, session: AsyncSession) -> AuthResponse:
        user_query = await session.execute(
            select(User).where(User.username == form_data.username)
        )

        db_user = user_query.scalar()

        if not db_user or not AuthController.pwd_context.verify(form_data.password, db_user.password_hash):
            raise HTTPException(status_code=401, detail="Incorrect username or password")

        # Генерация токенов с использованием id и username
        access_token = AuthController.create_access_token(user_id=db_user.id, username=db_user.username)
        refresh_token = AuthController.create_refresh_token(user_id=db_user.id, username=db_user.username)

        return AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer"
        )
