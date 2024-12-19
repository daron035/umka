from src.application.user import dto
from src.domain.grade.entities import GradeEntity, SubjectEntity
from src.domain.user.entities import UserEntity
from src.infrastructure.postgres.models import GradeModel, SubjectModel, UserModel


def convert_user_entity_to_db_model(user: UserEntity) -> UserModel:
    return UserModel(
        id=user.id.to_raw(),
        first_name=user.full_name.first_name,
        last_name=user.full_name.last_name,
        telegram_id=user.telegram_id.to_raw(),
        deleted_at=user.deleted_at.to_raw(),
    )


def convert_db_model_to_user_dto(user: UserModel) -> dto.User:
    return dto.User(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        telegram_id=user.telegram_id,
    )


def convert_db_model_to_subject_entity(subj: SubjectModel) -> SubjectEntity:
    return SubjectEntity(
        oid=subj.id,
        name=subj.name,
        description=subj.description,
    )


def convert_grade_entity_to_db_model(grade: GradeEntity) -> GradeModel:
    return GradeModel(
        user_id=grade.user_id.to_raw(),
        subject_id=grade.subject.oid,
        score=grade.score.to_raw(),
    )
