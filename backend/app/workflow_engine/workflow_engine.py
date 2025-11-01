from typing import Any, Dict, List, Optional
import requests
import logging
from nodes.base_nodes import BaseNode, NodeType, NodeExecutionError
from context import ExecutionContext
from nodes.trigger_nodes import TriggerType

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

    def execute(self, trigger_name: str = None) -> ExecutionContext:
        logger.info(f"Starting workflow execution: {self.name}")
        execution_queue: List[BaseNode] = []
        executed: List[str] = []

        if trigger_name:
            trigger_node = self.get_node(trigger_name)
            if not trigger_node:
                self.context.add_error(f"Trigger node {trigger_name} not found")
                return self.context
            
            logger.info(f"Executing workflow '{self.name}' from external trigger: {trigger_name}")
            result = trigger_node.execute(self.context)
            if result:
                self.context.data = result
                execution_queue.extend(self.connections.get(trigger_node.name, []))
        else:
        # Manual execution (user clicks run)
            trigger_nodes = [
                node for node in self.nodes
                if node.type == NodeType.TRIGGER and getattr(node, "trigger_type", None) == TriggerType.MANUAL
            ]
            for trigger in trigger_nodes:
                logger.info(f"Firing manual trigger: {trigger.name}")
                result = trigger.execute(self.context)
                if result:
                    self.context.data = result
                    execution_queue.extend(self.connections.get(trigger.name, []))


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