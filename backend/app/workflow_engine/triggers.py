from enum import Enum

class TriggerType(Enum):
    MANUAL = "manual"
    CRON = "cron"
    INTERVAL = "interval"

class Trigger:
    def __init__(self, type: TriggerType):
        self.type = type

class ManualTrigger(Trigger):
    def __init__(self):
        super().__init__(TriggerType.MANUAL)

class CronTrigger(Trigger):
    def __init__(self, cron_expression: str, timezone: str = "UTC"):
        super().__init__(TriggerType.CRON)
        self.cron_expression = cron_expression
        self.timezone = timezone

class IntervalTrigger(Trigger):
    def __init__(self, interval_minutes: int):
        super().__init__(TriggerType.INTERVAL)
        self.interval_minutes = interval_minutes