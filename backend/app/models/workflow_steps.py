from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum
import uuid

class ServiceEnum(str, Enum):
    GMAIL = "gmail"
    SHEETS = "sheets"
    SLACK = "slack"
    WEBHOOK = "webhook"

class WorkflowSteps(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    workflow_id: uuid.UUID = Field(foreign_key="Workflows.id", nullable=False, index=True)
    step_order: int = Field(nullable=False)
    service: str = Field(index=True, nullable=False)
    action: str = Field(index=True, nullable=False)
    config: Optional[str] = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    __tablename__ = "WorkflowSteps"