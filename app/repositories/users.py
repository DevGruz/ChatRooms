from app.utils.repository import SQLAlchemyRepository
from app.models.users import User


class UsersRepository(SQLAlchemyRepository):
    model = User
