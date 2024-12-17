from src.application.user.exceptions import UserIdNotExistError
from src.application.user.interfaces.persistence import UserRepo
from src.domain.user import entities
from src.domain.user.value_objects import UserId


class UserRepoMock(UserRepo):
    # TODO UserId -> User
    def __init__(self) -> None:
        self.users: dict[UserId, entities.User] = {}

    # async def exists_user_by_tg_id(self, tg_user_id: TgUserId) -> bool:
    #     return tg_user_id.to_raw() in self.users

    async def add_user(self, user: entities.User) -> None:
        self.users[user.id] = user

    async def update_user(self, user: entities.User) -> None:
        self.users[user.id] = user

