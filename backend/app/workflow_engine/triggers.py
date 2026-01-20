from enum import Enum
from dataclasses import dataclass
from croniter import croniter

class InvalidTrigger(Exception):
    pass

class TriggerType(Enum):
    MANUAL = "manual"
    CRON = "cron"
    INTERVAL = "interval"

@dataclass(frozen=True)
class Trigger:
    def __init__(self, type: TriggerType):
        self.type = type

@dataclass(frozen=True)
class ManualTrigger(Trigger):
    def __init__(self):
        super().__init__(TriggerType.MANUAL)

@dataclass(frozen=True)
class CronTrigger(Trigger):
    def __init__(self, cron_expression: str, timezone: str = "UTC"):

        if not croniter.is_valid(cron_expression):
            raise InvalidTrigger("Invalid cron expression")

        super().__init__(TriggerType.CRON)
        self.cron_expression = cron_expression
        self.timezone = timezone

@dataclass(frozen=True)
class IntervalTrigger(Trigger):
    def __init__(self, interval_minutes: int):
        super().__init__(TriggerType.INTERVAL)
        self.interval_minutes = interval_minutes