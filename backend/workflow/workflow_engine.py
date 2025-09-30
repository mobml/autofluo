from enum import Enum
import requests
import smtplib

class ExecutionContext:
    def __init__(self):
        self.data = {}
        self.history = []

class NodeType(Enum):
    TRIGGER = "trigger"
    HTTPREQUEST = "http_request"
    TRANSFORM = "transform"
    SENDEMAIL = "send_email"

class Node:
    name: str
    type: NodeType
    parameters: dict

    def __init__(self, name: str, type: NodeType, parameters: dict):
        self.name = name
        self.type = type
        self.parameters = parameters

class Workflow:
    name: str
    nodes: list[Node]
    connections: dict[str, list[Node]]

    def __init__(self, name: str, nodes: list[Node]):
        self.name = name
        self.nodes = nodes
        self.connections = {}

    def add_node(self, node: Node):
        self.nodes.append(node)

    def get_node(self, name: str) -> Node | None:
        for node in self.nodes:
            if node.name == name:
                return node
        return None
    
    def execute(self):
        context = ExecutionContext()
        execution_deque: list[Node] = []
        execution_deque.extend(self.connections["trigger"])
        executed: list[str] = []
        while execution_deque:
            current_node = execution_deque.pop(0)
            if current_node.name not in executed:
                print(f"Executing node: {current_node.name} of type {current_node.type}")

                if current_node.type == NodeType.TRIGGER:
                    print("Trigger node activated.")

                elif current_node.type == NodeType.HTTPREQUEST:
                    url = current_node.parameters.get("url")
                    try:
                        response = requests.get(url)
                        response.raise_for_status()
                        context.data = response.json()
                        print(f"GET request to {url} -> {response.json()}")
                    except Exception as e:
                        print(f"HTTP request failed: {e}")
                        context.data = {}

                elif current_node.type == NodeType.TRANSFORM:
                    operation = current_node.parameters.get("operation")
                    if operation == "uppercase" and isinstance(context.data, str):
                        context.data = context.data.upper()
                    elif operation == "extract_field":
                        field = current_node.parameters.get("field")
                        if isinstance(context.data, dict):
                            context.data = context.data.get(field)
                    print(f"Transformed -> {context.data}")

                elif current_node.type == NodeType.SENDEMAIL:
                    recipient = current_node.parameters.get("to")
                    print(f"Sending fake email to {recipient} -> subject: 'Test', body: 'Hello!'")

                executed.extend(current_node.name)
                if current_node.name in self.connections:
                    execution_deque.extend(self.connections[current_node.name])

workflow = Workflow(name="Sample Workflow", nodes=[])

trigger_node = Node(name="trigger", type=NodeType.TRIGGER, parameters={})
http_node = Node(name="http_request", type=NodeType.HTTPREQUEST, parameters={"url": "https://jsonplaceholder.typicode.com/posts/1"})
transform_node = Node(name="transform", type=NodeType.TRANSFORM, parameters={"operation": "extract_field", "field": "title"})
email_node = Node(name="send_email", type=NodeType.SENDEMAIL, parameters={"to": "example@gmail.com "})
email_node2 = Node(name="send_email_2", type=NodeType.SENDEMAIL, parameters={"to": "example2@gmail.com"})

workflow.add_node(trigger_node)
workflow.add_node(http_node)
workflow.add_node(transform_node)
workflow.add_node(email_node)
workflow.add_node(email_node2)

workflow.connections = {
    "trigger": [http_node],
    "http_request": [email_node2, transform_node],
    "transform": [email_node]
}

workflow.execute()