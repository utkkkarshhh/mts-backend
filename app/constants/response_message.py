from enum import Enum

class ResponseMessages(Enum):
    SERVICE_IS_UP = "Service is up and running"
    TASKS_QUEUED_SUCCESSFULLY = "Tasks Queued Successfully"
    INVALID_PRIORITY_LEVEL = "Invalid Priority Level"
    INVALID_PERCENTAGE_VALUE= "Invalid Percentage Value (must be greater than 0 and lesser than 100)"
    INVALID_PERCENTAGE_SUM = "Invalid Percentage Sum (must be 100 across all levels)"
    INVALID_EXECUTION_CONTEXT = "Invalid Execution Context"
    FAILED_TO_CREATE_TASK_BATCH = "Failed to create task batch."
