from enum import Enum
from dataclasses import dataclass, field
from croniter import croniter


class InvalidTrigger(Exception):
    pass


class TriggerType(Enum):
    MANUAL = "manual"
    CRON = "cron"
    INTERVAL = "interval"


@dataclass
class Trigger:
    type: TriggerType = field(init=False)


@dataclass
class ManualTrigger(Trigger):
    def __post_init__(self):
        self.type = TriggerType.MANUAL


@dataclass
class CronTrigger(Trigger):
    cron_expression: str
    timezone: str = "UTC"

    def __post_init__(self):
        if not croniter.is_valid(self.cron_expression):
            raise InvalidTrigger("Invalid cron expression")

        self.type = TriggerType.CRON


@dataclass
class IntervalTrigger(Trigger):
    interval_minutes: int

    def __post_init__(self):
        if self.interval_minutes <= 0:
            raise InvalidTrigger("Interval must be positive")

        self.type = TriggerType.INTERVAL
