import json
import logging
import requests
from typing import Any, Dict

from nodes.base_nodes import BaseNode, NodeType, NodeExecutionError
from context import ExecutionContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HttpRequestNode(BaseNode):
    def __init__(self, name: str, parameters: Dict[str, Any]):
        super().__init__(name, parameters)
        self.type = NodeType.HTTPREQUEST

    def validate_parameters(self):
        if "url" not in self.parameters:
            raise NodeExecutionError("Missing required parameter: url")
        return True

    def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        self.validate_parameters()

        url = self.parameters["url"]
        method = self.parameters.get("method", "GET").upper()
        headers = self.parameters.get("headers", {})
        body = self.parameters.get("body", None)

        logger.info(f"[HTTP] {method} {url}")

        try:
            response = requests.request(
                method=method,
                url=url,
                json=body,
                headers=headers,
                timeout=10
            )
        except Exception as e:
            error_message = f"HTTP request failed: {str(e)}"
            context.add_error(error_message)
            raise NodeExecutionError(error_message)

        result = {
            "status": response.status_code,
            "success": response.ok,
            "raw": response.text
        }

        try:
            result["body"] = response.json()
        except json.JSONDecodeError:
            result["body"] = None


        context.set(self.name, result)

        context.add_history(self.name)

        return result