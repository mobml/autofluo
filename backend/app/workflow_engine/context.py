from typing import Any, Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExecutionContext:
    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.history: List[str] = []
        self.errors: List[str] = []

    def set(self, key: str, value: Any):
        """Store data globally accessible to other nodes."""
        logger.info(f"[CONTEXT] Set {key} = {value}")
        self.data[key] = value

    def get(self, key: str) -> Optional[Any]:
        """Retrieve data stored by another node."""
        return self.data.get(key)
    
    def add_history(self, node_name: str):
        """Record executed node."""
        self.history.append(node_name)

    def add_error(self, error: str):
        self.errors.append(error)
        logger.error(error)