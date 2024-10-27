from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from src.ml.rec_employees import evaluate_employees

from src.Schemas.UserSchemas import UserOutput
from src.Schemas.AiSchemas import AiInput

from src.Models.UserMeta import UserMeta
from src.Models.User import User
from src.Models.MasterTask import MasterTask
from src.Models.Position import Position

from src.Controllers.UserController import UserController
from src.Controllers.UserMetaController import UserMetaController
from src.Controllers.MasterTaskController import MasterTaskController
from src.Controllers.PositionController import PositionController

class AiController:
    
    @staticmethod
    async def get_rec_users(data: AiInput, session: AsyncSession) -> List[UserOutput]:
        users = await UserController.get_all(session)
        user_ids = [u.id for u in users]
        indexed_users = {id:item for id, item in zip(user_ids, users)}
        users_meta = await UserMetaController.get_all(session)

        dict_users = []
        for um in users_meta:
            position = await PositionController.get_one(um.position_id, session)

            dict_users.append({
                'id':indexed_users[um.user_id].id,
                'fullname':indexed_users[um.user_id].fullname,
                'position':position.name,
                'description':um.description,
                'stack':um.stack,
                'rating':um.rating
            })

        master_task = await MasterTaskController.get_one(data.master_task_id, session)

        results = await evaluate_employees(dict_users, master_task.name, data.stack)
        ids = [user['id'] for user in results]
        return [indexed_users[id] for id in ids]