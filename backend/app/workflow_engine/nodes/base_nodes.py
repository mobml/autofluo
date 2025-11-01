from enum import Enum
from abc import ABC, abstractmethod
from typing import Any, Dict
from context import ExecutionContext

class NodeType(Enum):
    TRIGGER = "trigger"
    HTTPREQUEST = "http_request"
    TRANSFORM = "transform"
    SENDEMAIL = "send_email"

class NodeExecutionError(Exception):
    """Custom exception for node execution errors"""
    pass

class BaseNode(ABC):
    def __init__(self, name: str, parameters: Dict[str, Any]):
        self.name = name
        self.parameters = parameters

    @abstractmethod
    def execute(self, context: ExecutionContext) -> Any:
        pass

    def validate_parameters(self) -> bool:
        """Override this method to add parameter validation"""
        return True
