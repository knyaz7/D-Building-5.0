from datetime import datetime

from src.Config.db import get_session
from src.Controllers.RoleController import RoleController
from src.Controllers.StageController import StageController
from src.Controllers.UserController import UserController
from src.Controllers.UserMetaController import UserMetaController
from src.Schemas.RoleSchemas import RoleInput
from src.Schemas.StageSchemas import StageInput
from src.Schemas.UserMetaSchemas import UserMetaInput
from src.Schemas.UserSchemas import UserInput, UserInputUpdate


class SeederHelper:
    stages = ["To Do", "To Do Faster", "In Progress", "Testing", "Done"]
    roles = ["admin", "employee", "guest"]
    user = UserInput(username="Bebrbulinka", fullname="Еремеева Вероника Ервандовна", password="qwerty")
    user_meta = UserMetaInput(user_id=1, description="idk", employed_at=datetime.utcnow())

    @staticmethod
    async def run_seeder():
        await SeederHelper.create_roles()
        await SeederHelper.create_stages()
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
    async def create_user():
        async for session in get_session():
            users = await UserController.get_all(session)
            if not users:
                await UserController.create(SeederHelper.user, session)
                upd_user = UserInputUpdate(username="Bebrbulinka", fullname="Еремеева Вероника Ервандовна", role_id=1)
                await UserController.update(1, upd_user, session)

            user_meta = await UserMetaController.get_all(session)
            if not user_meta:
                await UserMetaController.create(SeederHelper.user_meta, session)

