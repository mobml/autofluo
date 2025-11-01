from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from workflow_engine import Workflow
import logging

logger = logging.getLogger(__name__)

class WorkflowScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.workflows = []

    def register_workflow(self, workflow: Workflow):
        """Register a workflow and its schedule triggers"""
        self.workflows.append(workflow)
        for node in workflow.nodes:
            if node.type.value == "trigger" and hasattr(node, "parameters"):
                schedule_type = node.parameters.get("schedule_type")
                
                if schedule_type == "cron":
                    cron_expr = node.parameters.get("cron_expression")
                    timezone = node.parameters.get("timezone", "UTC")
                    self.scheduler.add_job(
                        self.run_workflow,
                        CronTrigger.from_crontab(cron_expr, timezone=timezone),
                        args=[workflow, node.name],
                        id=f"{workflow.name}-{node.name}"
                    )
                    logger.info(f"Registered cron job for {workflow.name}: {cron_expr}")

                elif schedule_type == "interval":
                    minutes = node.parameters.get("interval_minutes", 5)
                    self.scheduler.add_job(
                        self.run_workflow,
                        IntervalTrigger(minutes=minutes),
                        args=[workflow, node.name],
                        id=f"{workflow.name}-{node.name}"
                    )
                    logger.info(f"Registered interval job for {workflow.name}: every {minutes}m")

    def run_workflow(self, workflow: Workflow, trigger_name: str):
        logger.info(f"Executing scheduled workflow {workflow.name} via {trigger_name}")
        workflow.execute(trigger_name=trigger_name)

    def start(self):
        logger.info("Starting workflow scheduler...")
        self.scheduler.start()

    def shutdown(self):
        logger.info("Shutting down scheduler...")
        self.scheduler.shutdown()