from sqlalchemy.orm import Session
from models.user import User
import sqlmodel

class UserRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create_user(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_user_by_username(self, username: str) -> User | None:
        q = sqlmodel.select(User).where(User.username == username)
        result = self.session.execute(q)
        return result.scalar_one_or_none()

    def get_user_by_id(self, user_id: str) -> User | None:
        q = sqlmodel.select(User).where(User.id == user_id)
        result = self.session.execute(q)
        return result.scalar_one_or_none()
        