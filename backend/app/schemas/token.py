from pydantic import BaseModel
from app.schemas.user import UserRead

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserInDB(UserRead):
    hashed_password: str