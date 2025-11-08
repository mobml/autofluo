import yagmail
import logging
from typing import Dict, Any
from nodes.base_nodes import BaseNode, NodeType, NodeExecutionError
from context import ExecutionContext
from jinja2 import Template

logger = logging.getLogger(__name__)

class SendEmailNode(BaseNode):
    def __init__(self, name: str, parameters: Dict[str, Any]):
        super().__init__(name, parameters)
        self.type = NodeType.SENDEMAIL

    def validate_parameters(self):
        required = ["from_email", "app_password", "to", "subject", "body"]
        for param in required:
            if param not in self.parameters:
                raise NodeExecutionError(f"Missing required parameter: {param}")
        return True

    def _render(self, template_str: str, context: ExecutionContext) -> str:
        """
        Rindea texto usando variables guardadas en el contexto.
        Ejemplo: "Hola {{ GetTodo.body.title }}"
        """
        try:
            template = Template(template_str)
            return template.render(**context.data)
        except Exception as e:
            raise NodeExecutionError(f"Template rendering failed: {e}")

    def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        self.validate_parameters()

        from_email = self.parameters["from_email"]
        app_password = self.parameters["app_password"]
        to = self.parameters["to"]

        subject = self._render(self.parameters["subject"], context)
        body = self._render(self.parameters["body"], context)

        logger.info(f"[EMAIL] Sending Gmail message to {to}")

        try:
            yag = yagmail.SMTP(from_email, app_password)
            yag.send(to=to, subject=subject, contents=body)
        except Exception as e:
            error_message = f"Failed to send email via Gmail: {e}"
            context.add_error(error_message)
            raise NodeExecutionError(error_message)

        result = {
            "success": True,
            "provider": "gmail",
            "sent_to": to,
            "subject": subject,
            "body": body
        }

        context.set(self.name, result)
        context.add_history(self.name)

        return result