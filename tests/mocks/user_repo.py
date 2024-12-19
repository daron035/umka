from src.application.user.exceptions import UserIdNotExistError
from src.application.user.interfaces.persistence import UserRepo
from src.domain.user import entities
from src.domain.user.value_objects import UserId


class UserRepoMock(UserRepo):
    # TODO UserId -> User
    def __init__(self) -> None:
        self.users: dict[UserId, entities.User] = {}

    async def add_user(self, user: entities.User) -> None:
        self.users[user.id] = user

    async def update_user(self, user: entities.User) -> None:
        self.users[user.id] = user

