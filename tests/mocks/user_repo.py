from src.application.user.exceptions import UserIdNotExistError
from src.application.user.interfaces.persistence import UserRepo
from src.domain.user.entities import UserEntity
from src.domain.user.value_objects import UserId
from src.domain.user.value_objects.tg_user_id import TgUserId


class UserRepoMock(UserRepo):
    def __init__(self) -> None:
        self.users: dict[UserId, UserEntity] = {}

    async def add_user(self, user: UserEntity) -> None:
        self.users[user.id] = user

    async def exists_user_by_tg_id(self, tg_user_id: TgUserId) -> bool:
        return any(user.telegram_id == tg_user_id for user in self.users.values())

