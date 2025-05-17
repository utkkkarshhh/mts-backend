from typing import Any, Callable

from app.constants import Constants, ResponseMessages
from app.models import TaskBatch
from app.utils import Helper, logger
from app.exceptions import BadRequestException


class TaskManager(Helper):
    @classmethod
    async def schedule_tasks(cls, tasks: dict[str, Callable]):
        logger.info("Scheduling tasks...")
        task_batch_object = await cls._process_tasks(tasks)
        if not task_batch_object:
            logger.error(ResponseMessages.FAILED_TO_CREATE_TASK_BATCH.value)
            raise BadRequestException(ResponseMessages.FAILED_TO_CREATE_TASK_BATCH.value)
        logger.info(f"========== total_count: {task_batch_object.total_count} =============")


    @classmethod
    async def _process_tasks(cls, tasks: dict[str, Callable]):
        total_tasks = tasks.get('total_count')
        priority_groups = tasks.get('priorities')
        priority_groups = cls.validate_and_update_priority_group_data(priority_groups, total_tasks)
        task_batch_object = await cls._create_task_batch(total_count=total_tasks, priority_config=priority_groups)
        return task_batch_object
        
    @classmethod   
    async def _create_task_batch(cls, total_count: int, priority_config: dict):
        task_batch_object = await TaskBatch.create(
            total_count=total_count,
            priority_config=priority_config,
            status=Constants.TASK_STATUS.get('PENDING'),
            success_count=0,
            failure_count=0,
            created_at=cls.get_current_time(),
            completed_at=None
        )
        return task_batch_object