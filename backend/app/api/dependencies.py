from fastapi import Depends
from database import get_session
from sqlmodel import Session
from app.services.user_service import UserService
from app.repository.user_repository import UserRepository

def get_user_service(session: Session = Depends(get_session)) -> UserService:
    repo = UserRepository(session)
    return UserService(repo)