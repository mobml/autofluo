from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.config import settings
from app.core.security import create_access_token
from services.auth import authenticate_user
from services.user_service import UserService
from app.repository.user_repository import UserRepository
from app.schemas.token import Token
from database import get_session
from sqlmodel import Session

router = APIRouter(
    prefix="/token",
    tags=["auth"],
)

def get_user_service(session: Session = Depends(get_session)) -> UserService:
    repo = UserRepository(session)
    return UserService(repo)

@router.post("/")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(get_user_service),
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, user_service)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")