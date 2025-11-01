from typing import Any, Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExecutionContext:
    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.history: List[str] = []
        self.errors: List[str] = []

    def add_error(self, error: str):
        self.errors.append(error)
        logger.error(error)
