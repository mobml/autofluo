from nodes import BaseNode
from triggers import Trigger
from uuid import UUID
from triggers import TriggerType

class Workflow:
    def __init__(
        self,
        id: UUID,
        name: str,
        nodes: list[BaseNode],
        connections: dict,
        triggers: list[Trigger],
        is_active: bool = False
    ):
        self.id = id
        self.name = name
        self.nodes = nodes
        self.connections = connections
        self.triggers = triggers
        self.is_active = is_active

        if not nodes:
            raise ValueError("A workflow must contain at least one node.")
        if not triggers:
            raise ValueError("A workflow must have at least one trigger.")

    def has_manual_trigger(self) -> bool:
        return any(t.type == TriggerType.MANUAL for t in self.triggers)

    def scheduled_triggers(self) -> list:
        return [t for t in self.triggers if t.type in (TriggerType.CRON, TriggerType.INTERVAL)]