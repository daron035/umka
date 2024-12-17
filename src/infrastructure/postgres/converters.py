from src.domain.user import (
    entities,
)
from src.infrastructure.postgres import models


def convert_user_entity_to_db_model(user: entities.User) -> models.User:
    return models.User(
        id=user.id.to_raw(),
        first_name=user.full_name.first_name,
        last_name=user.full_name.last_name,
        telegram_id=user.telegram_id,
        deleted_at=user.deleted_at.to_raw(),
    )
