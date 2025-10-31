from app.schemas.user import UserCreate
from repository.user_repository import UserRepository
from app.core.security import get_password_hash
from models.user import User


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def create_user(self, user: UserCreate) -> User:
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=get_password_hash(user.hashed_password),
        )
        return self.user_repo.create_user(db_user)

    def get_user_by_username(self, username: str) -> User | None:
        return self.user_repo.get_user_by_username(username)