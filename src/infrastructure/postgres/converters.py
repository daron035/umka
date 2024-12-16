from src.domain.user import (
    entities,
)
from src.infrastructure.postgres import models


def convert_user_entity_to_db_model(user: entities.User) -> models.User:
    return models.User(
        id=user.id.to_raw(),
        first_name=user.full_name.first_name,
        last_name=user.full_name.last_name,
        middle_name=user.full_name.middle_name,
        deleted_at=user.deleted_at.to_raw(),
    )
