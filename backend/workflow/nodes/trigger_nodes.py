from enum import Enum
from abc import abstractmethod
from datetime import datetime
from typing import Any, Dict
from croniter import croniter
import pytz
from nodes.base_nodes import BaseNode, NodeType, NodeExecutionError
from context import ExecutionContext
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TriggerType(Enum):
    MANUAL = "manual"
    SCHEDULE = "schedule"
    WEBHOOK = "webhook"

class BaseTrigger(BaseNode):
    def __init__(self, name: str, trigger_type: TriggerType, parameters: Dict[str, Any]):
        super().__init__(name, parameters)
        self.type = NodeType.TRIGGER
        self.trigger_type = trigger_type

class ManualTrigger(BaseTrigger):
    def __init__(self, name: str, parameters: Dict[str, Any]):
        super().__init__(name, TriggerType.MANUAL, parameters)

    def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        logger.info("Manual trigger activated")
        return {
            "trigger_type": "manual",
            "timestamp": datetime.now().isoformat()
        }

class ScheduleTrigger(BaseTrigger):
    def __init__(self, name: str, parameters: Dict[str, Any]):
        super().__init__(name, TriggerType.SCHEDULE, parameters)
        self.timezone = parameters.get("timezone", "UTC")
        self.last_execution = None
        self._validate_schedule_parameters()

    def _validate_schedule_parameters(self):
        schedule_type = self.parameters.get("schedule_type")
        if not schedule_type:
            raise NodeExecutionError("schedule_type is required (interval or cron)")
            
        if schedule_type == "cron":
            cron_expr = self.parameters.get("cron_expression")
            if not cron_expr or not croniter.is_valid(cron_expr):
                raise NodeExecutionError("Invalid cron expression")
        elif schedule_type == "interval":
            if "interval_minutes" not in self.parameters:
                raise NodeExecutionError("interval_minutes is required for interval schedule")

    def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        logger.info("Schedule trigger activated")
        now = datetime.now(pytz.timezone(self.timezone))
        self.last_execution = now
        return {
            "trigger_type": "schedule",
            "schedule_type": self.parameters["schedule_type"],
            "timestamp": now.isoformat(),
            "timezone": self.timezone
        }