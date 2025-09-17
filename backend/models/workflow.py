from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

class Workflow(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    user_id: uuid.UUID = Field(foreign_key="Users.id", nullable=False, index=True)
    name: str = Field(index=True, unique=True, nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)

    __tablename__ = "Workflows"