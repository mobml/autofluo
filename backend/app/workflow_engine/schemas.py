from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class Node(BaseModel):
    id: str
    name: str
    type: str  # http_request, data_transform, condition, etc.
    parameters: Dict[str, Any]
    position: List[float]
    disabled: bool = False

class Connection(BaseModel):
    source_node: str
    source_output: str = "main"
    target_node: str
    target_input: str = "main"

class WorkflowSchema(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = ""
    nodes: List[Node]
    connections: List[Connection]
    is_active: bool = False

class ExecutionResult(BaseModel):
    node_id: str
    status: str
    data: Any
    error: Optional[str] = None
    execution_time_ms: int