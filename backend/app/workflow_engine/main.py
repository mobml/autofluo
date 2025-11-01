from scheduler import WorkflowScheduler
from workflow_engine import Workflow, HttpRequestNode
from nodes.trigger_nodes import ManualTrigger, ScheduleTrigger

# Example workflow creation
def create_sample_workflow() -> Workflow:
    workflow = Workflow(name="Sample Workflow")

    # Create different types of triggers
    manual_trigger = ManualTrigger("manual_trigger", {})
    
    schedule_trigger = ScheduleTrigger("cron_trigger", {
        "schedule_type": "cron",
        "cron_expression": "*/2 * * * *",  # Every two minutes
        "timezone": "UTC"
    })

    interval_trigger = ScheduleTrigger("interval_trigger", {
        "schedule_type": "interval",
        "interval_minutes": 1,  # Every 1 minute
        "timezone": "UTC"
    })

    interval_trigger_2 = ScheduleTrigger("interval_trigger_2_min", {
        "schedule_type": "interval",
        "interval_minutes": 2,  # Every 2 minutes
        "timezone": "UTC"
    })

    http = HttpRequestNode("http_request", {
        "url": "https://jsonplaceholder.typicode.com/posts/1"
    })
    
    # Add nodes to workflow
    workflow.add_node(manual_trigger)
    #workflow.add_node(schedule_trigger)
    workflow.add_node(interval_trigger)
    workflow.add_node(interval_trigger_2)
    workflow.add_node(http)

    # Set up connections
    workflow.add_connection("manual_trigger", [http])
    #workflow.add_connection("cron_trigger", [http])
    workflow.add_connection("interval_trigger", [http])
    workflow.add_connection("interval_trigger_2_min", [http])

    return workflow

if __name__ == "__main__":
    workflow = create_sample_workflow()

    scheduler = WorkflowScheduler()
    scheduler.register_workflow(workflow)
    scheduler.start()

    workflow.execute()  # Initial manual run
    try: 
        while True:
            pass  # Keep the main thread alive
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
    
    #result = workflow.execute()