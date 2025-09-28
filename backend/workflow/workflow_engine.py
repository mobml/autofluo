from enum import Enum

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
        execution_deque: list[Node] = []
        execution_deque.extend(self.connections["trigger"])
        executed: list[str] = []
        while execution_deque:
            current_node = execution_deque.pop(0)
            if current_node.name not in executed:
                print(f"Executing node: {current_node.name} of type {current_node.type}")
                executed.extend(current_node.name)
                if current_node.name in self.connections:
                    execution_deque.extend(self.connections[current_node.name])

workflow = Workflow(name="Sample Workflow", nodes=[])

trigger_node = Node(name="trigger", type=NodeType.TRIGGER, parameters={})
http_node = Node(name="http_request", type=NodeType.HTTPREQUEST, parameters={"url": "https://api.example.com/data"})
transform_node = Node(name="transform", type=NodeType.TRANSFORM, parameters={"operation": "uppercase"})
email_node = Node(name="send_email", type=NodeType.SENDEMAIL, parameters={"to": "from"})

workflow.add_node(trigger_node)
workflow.add_node(http_node)
workflow.add_node(transform_node)
workflow.add_node(email_node)

workflow.connections = {
    "trigger": [http_node],
    "http_request": [transform_node],
    "transform": [email_node]
}

workflow.execute()