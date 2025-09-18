from fastapi import APIRouter, Depends, HTTPException, status
from schema.user import UserCreate, UserRead
from typing import Annotated
from services.auth import get_current_active_user
from services import user_service
from sqlmodel import Session
from database import get_session
from services.user_service import get_user_by_username

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/me/", response_model=UserRead)
async def read_users_me(
    current_user: Annotated[UserRead, Depends(get_current_active_user)],
):
    return current_user


@router.get("/me/items/")
async def read_own_items(
    current_user: Annotated[UserRead, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_session)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return user_service.create_user(db=db, user=user)