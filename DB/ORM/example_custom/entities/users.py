from decorators import db_entity
from enums.db_type import DbColumnType
from models.db_column import DbColumn


@db_entity("users")
class User():
    user_id: int = DbColumn("user_id", DbColumnType.INTEGER, primary_key=True)
    username: str = DbColumn("username", DbColumnType.VARCHAR, unique=True)