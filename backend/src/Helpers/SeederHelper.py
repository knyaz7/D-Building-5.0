from datetime import datetime

from src.Config.db import get_session
from src.Controllers.PositionController import PositionController
from src.Controllers.RoleController import RoleController
from src.Controllers.StageController import StageController
from src.Controllers.ToolController import ToolController
from src.Controllers.UserController import UserController
from src.Controllers.UserMetaController import UserMetaController
from src.Schemas.PositionSchemas import PositionInput
from src.Schemas.RoleSchemas import RoleInput
from src.Schemas.StageSchemas import StageInput
from src.Schemas.ToolSchemas import ToolInput
from src.Schemas.UserMetaSchemas import UserMetaInput
from src.Schemas.UserSchemas import UserInput, UserInputUpdate


class SeederHelper:
    stages = ["To Do", "To Do Faster", "In Progress", "Testing", "Done"]
    roles = ["admin", "employee", "guest"]
    positions = ["Аналитик", "Тестировщик", "Бэкендер", "Фронтендер", "ML-разработчик"]
    stacks = ["pytest", "fastapi", "postgreSQL", "sqlalchemy", "quasar", "tensorflow"]
    users = [
        UserInput(username="Bebrbulinka", fullname="Еремеева Вероника Ервандовна", password="qwerty"),
        UserInput(username="user2", fullname="Баранов Иван Ервандович", password="qwerty"),
        UserInput(username="user3", fullname="Козлов Петр Ервандович", password="qwerty"),
        UserInput(username="user4", fullname="Лосева Евгения Ервандовна", password="qwerty"),
        UserInput(username="user5", fullname="Китова Кристина Ервандовна", password="qwerty"),
        UserInput(username="user6", fullname="Быков Андрей Ервандович", password="qwerty"),
        UserInput(username="user7", fullname="Гусева Геннадия Ервандовна", password="qwerty")
    ]
    user_metas = [
        UserMetaInput(user_id=1, position_id=1, stack=[], description="Анализирует идеально, нареканий нет", rating=100, employed_at=datetime.utcnow()),
        UserMetaInput(user_id=2, position_id=2, stack=[1], description="Умеет писать только UNIT тесты", rating=70, employed_at=datetime.utcnow()),
        UserMetaInput(user_id=3, position_id=3, stack=[2, 3, 4], description="Плохо понимает миграции", rating=60, employed_at=datetime.utcnow()),
        UserMetaInput(user_id=4, position_id=4, stack=[5], description="Иногда забывает что такое HTML", rating=50, employed_at=datetime.utcnow()),
        UserMetaInput(user_id=5, position_id=5, stack=[6], description="Знает что такое tensorflow", rating=90, employed_at=datetime.utcnow()),
        UserMetaInput(user_id=6, position_id=1, stack=[], description="Анализирует раз через раз", rating=50, employed_at=datetime.utcnow()),
        UserMetaInput(user_id=7, position_id=2, stack=[1], description="Умеет писать все виды тестов", rating=100, employed_at=datetime.utcnow()),
    ]

    @staticmethod
    async def run_seeder():
        await SeederHelper.create_stages()
        await SeederHelper.create_roles()
        await SeederHelper.create_positions()
        await SeederHelper.create_tools()
        await SeederHelper.create_user()

    @staticmethod
    async def create_stages():
        async for session in get_session():
            stages = await StageController.get_all(session)
            if not stages:
                for stage in SeederHelper.stages:
                    await StageController.create(StageInput(name=stage), session)

    @staticmethod
    async def create_roles():
        async for session in get_session():
            roles = await RoleController.get_all(session)
            if not roles:
                for role in SeederHelper.roles:
                    await RoleController.create(RoleInput(name=role), session)

    @staticmethod
    async def create_positions():
        async for session in get_session():
            positions = await PositionController.get_all(session)
            if not positions:
                for position in SeederHelper.positions:
                    await PositionController.create(PositionInput(name=position), session)

    @staticmethod
    async def create_tools():
        async for session in get_session():
            tools = await ToolController.get_all(session)
            if not tools:
                for tool in SeederHelper.stacks:
                    await ToolController.create(ToolInput(name=tool), session)

    @staticmethod
    async def create_user():
        async for session in get_session():
            users = await UserController.get_all(session)
            if not users:
                for user in SeederHelper.users:
                    await UserController.create(user, session)
                upd_user = UserInputUpdate(username="Bebrbulinka", fullname="Еремеева Вероника Ервандовна", role_id=1)
                await UserController.update(1, upd_user, session)

            user_metas = await UserMetaController.get_all(session)
            if not user_metas:
                for user_meta in SeederHelper.user_metas:
                    await UserMetaController.create(user_meta, session)

