from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum
import uuid

class StatusEnum(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Execution(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    workflow_id: uuid.UUID = Field(foreign_key="Workflows.id", nullable=False, index=True)
    status: StatusEnum = Field(index=True, default=StatusEnum.PENDING, nullable=False)
    started_at: datetime = Field(default_factory=datetime.now, nullable=False)
    completed_at: Optional[datetime] = Field(default=None, nullable=True)
    log: Optional[str] = Field(default=None, nullable=True)
    __tablename__ = "Executions"