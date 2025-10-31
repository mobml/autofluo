from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    username: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    __tablename__ = "Users"