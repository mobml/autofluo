from app.schemas.user import UserCreate, UserRead
from sqlalchemy.orm import Session
from core.security import get_password_hash
from models.user import User
import sqlmodel

def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.hashed_password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str) -> User | None:
    q = sqlmodel.select(User).where(User.username == username)
    result = db.execute(q)
    return result.scalar_one_or_none()

def get_user_by_id(db: Session, user_id: str) -> User | None:
    q = sqlmodel.select(User).where(User.id == user_id)
    result = db.execute(q)
    return result.scalar_one_or_none()