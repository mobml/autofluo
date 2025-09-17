from pydantic import BaseModel
import uuid

class UserCreate(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    hashed_password: str
    is_active: bool

class UserRead(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    hashed_password: str
    is_active: bool
    created_at: str