from enum import Enum
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import requests
import smtplib
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NodeType(Enum):
    TRIGGER = "trigger"
    HTTPREQUEST = "http_request"
    TRANSFORM = "transform"
    SENDEMAIL = "send_email"

class ExecutionContext:
    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.history: List[str] = []
        self.errors: List[str] = []

    def add_error(self, error: str):
        self.errors.append(error)
        logger.error(error)

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

class TriggerNode(BaseNode):
    def __init__(self, name: str, parameters: Dict[str, Any]):
        super().__init__(name, parameters)
        self.type = NodeType.TRIGGER

    def execute(self, context: ExecutionContext) -> bool:
        logger.info("Trigger node activated")
        return True

class HttpRequestNode(BaseNode):
    def __init__(self, name: str, parameters: Dict[str, Any]):
        super().__init__(name, parameters)
        self.type = NodeType.HTTPREQUEST
        
    def validate_parameters(self) -> bool:
        return "url" in self.parameters

    def execute(self, context: ExecutionContext) -> Any:
        if not self.validate_parameters():
            raise NodeExecutionError("URL parameter is required")
            
        url = self.parameters["url"]
        try:
            response = requests.get(url)
            response.raise_for_status()
            result = response.json()
            logger.info(f"GET request to {url} successful")
            return result
        except Exception as e:
            error_msg = f"HTTP request failed: {str(e)}"
            context.add_error(error_msg)
            return {}

class TransformNode(BaseNode):
    VALID_OPERATIONS = ["uppercase", "extract_field"]

    def __init__(self, name: str, parameters: Dict[str, Any]):
        super().__init__(name, parameters)
        self.type = NodeType.TRANSFORM

    def validate_parameters(self) -> bool:
        operation = self.parameters.get("operation")
        return operation in self.VALID_OPERATIONS

    def execute(self, context: ExecutionContext) -> Any:
        if not self.validate_parameters():
            raise NodeExecutionError(f"Invalid operation. Must be one of {self.VALID_OPERATIONS}")

        operation = self.parameters["operation"]
        data = context.data

        if operation == "uppercase" and isinstance(data, str):
            result = data.upper()
        elif operation == "extract_field":
            field = self.parameters.get("field")
            if not field:
                raise NodeExecutionError("Field parameter is required for extract_field operation")
            if isinstance(data, dict):
                result = data.get(field)
            else:
                raise NodeExecutionError("Data must be a dictionary for extract_field operation")
        else:
            raise NodeExecutionError(f"Operation {operation} not implemented")

        logger.info(f"Transform operation {operation} completed")
        return result

class EmailNode(BaseNode):
    def __init__(self, name: str, parameters: Dict[str, Any]):
        super().__init__(name, parameters)
        self.type = NodeType.SENDEMAIL

    def validate_parameters(self) -> bool:
        return "to" in self.parameters

    def execute(self, context: ExecutionContext) -> None:
        if not self.validate_parameters():
            raise NodeExecutionError("Recipient (to) parameter is required")

        recipient = self.parameters["to"]
        # Implement actual email sending logic here
        logger.info(f"Email sent to {recipient}")
        return None

class Workflow:
    def __init__(self, name: str):
        self.name = name
        self.nodes: List[BaseNode] = []
        self.connections: Dict[str, List[BaseNode]] = {}
        self.context = ExecutionContext()

    def add_node(self, node: BaseNode) -> None:
        self.nodes.append(node)

    def get_node(self, name: str) -> Optional[BaseNode]:
        return next((node for node in self.nodes if node.name == name), None)

    def add_connection(self, from_node: str, to_nodes: List[BaseNode]) -> None:
        self.connections[from_node] = to_nodes

    def execute(self) -> ExecutionContext:
        logger.info(f"Starting workflow execution: {self.name}")
        execution_queue: List[BaseNode] = []
        executed: List[str] = []

        # Find trigger nodes to start execution
        trigger_nodes = [node for node in self.nodes if isinstance(node, TriggerNode)]
        execution_queue.extend(trigger_nodes)

        while execution_queue:
            current_node = execution_queue.pop(0)
            if current_node.name not in executed:
                try:
                    logger.info(f"Executing node: {current_node.name}")
                    self.context.data = current_node.execute(self.context)
                    executed.append(current_node.name)

                    # Add connected nodes to the queue
                    if current_node.name in self.connections:
                        execution_queue.extend(self.connections[current_node.name])

                except NodeExecutionError as e:
                    self.context.add_error(f"Error in node {current_node.name}: {str(e)}")
                except Exception as e:
                    self.context.add_error(f"Unexpected error in node {current_node.name}: {str(e)}")

        logger.info("Workflow execution completed")
        return self.context

# Example usage
def create_sample_workflow() -> Workflow:
    workflow = Workflow(name="Sample Workflow")

    # Create nodes
    trigger = TriggerNode("trigger", {})
    http = HttpRequestNode("http_request", {"url": "https://jsonplaceholder.typicode.com/posts/1"})
    transform = TransformNode("transform", {"operation": "extract_field", "field": "title"})
    email1 = EmailNode("send_email", {"to": "example@gmail.com"})
    email2 = EmailNode("send_email_2", {"to": "example2@gmail.com"})

    # Add nodes to workflow
    for node in [trigger, http, transform, email1, email2]:
        workflow.add_node(node)

    # Set up connections
    workflow.add_connection("trigger", [http])
    workflow.add_connection("http_request", [email2, transform])
    workflow.add_connection("transform", [email1])

    return workflow

if __name__ == "__main__":
    workflow = create_sample_workflow()
    result = workflow.execute()