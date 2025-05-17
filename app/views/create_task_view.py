from fastapi import status

from app.constants import ResponseMessages
from app.managers import TaskManager
from app.schemas import TaskRequest
from app.utils import ResponseHandler


class CreateTaskView():
    
    @staticmethod
    async def post(tasks_object: TaskRequest):
        tasks = tasks_object.dict().get('tasks')
        response = await TaskManager.schedule_tasks(tasks)
        return ResponseHandler(
            message=ResponseMessages.TASKS_QUEUED_SUCCESSFULLY,
            success=True,
            status=status.HTTP_200_OK
        )
