import json
import uuid
from typing import Any, Callable

from app.constants import Constants, PriorityQueues, ResponseMessages
from app.exceptions import BadRequestException
from app.models import TaskBatch
from app.redis.client import redis_client
from app.managers import JobExecutionManager
from app.utils import Helper, logger


class TaskManager(Helper):
    @classmethod
    async def schedule_tasks(cls, payload: dict[str, Callable]):
        task_batch_object = await cls._process_tasks(payload)
        if not task_batch_object:
            logger.error(ResponseMessages.FAILED_TO_CREATE_TASK_BATCH.value)
            raise BadRequestException(ResponseMessages.FAILED_TO_CREATE_TASK_BATCH.value)
        await cls._load_task_batch_in_redis(task_batch_object)
    
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
    
    @classmethod
    async def _load_task_batch_in_redis(cls, task_batch_object: TaskBatch):
        priority_config = task_batch_object.priority_config
        total_tasks = 0
        
        try:
            for priority_label, config in priority_config.items():
                logger.info(f"Processing priority_label: {priority_label}")
                queue = PriorityQueues.PRIORITY_TO_QUEUE.get(priority_label)
                
                if not queue:
                    continue
                
                logger.info(f"Queue: {queue.name}, Tasks to add: {config['count']}")
                
                for _ in range(config["count"]):
                    task = {
                        "id": str(uuid.uuid4()),
                        "priority": priority_label,
                        "execution_context": config.get("execution_context", {}),
                        "metadata": {},
                        "task_batch_id": str(task_batch_object.id)
                    }
                    logger.info(f"Enqueueing task: {json.dumps(task)}")
                    job = queue.enqueue(
                        JobExecutionManager.process_task_job,
                        kwargs={"task": task},
                        job_id=task["id"]
                    )
                    if job:
                        logger.info(f"Successfully enqueued job with ID: {job.id}")
                        total_tasks += 1
                    else:
                        logger.error(f"Failed to enqueue job for task: {task['id']}")
        
        except Exception as e:
            logger.error(f"Error enqueueing tasks: {str(e)}")
            raise
            
        logger.info(f"Enqueued {total_tasks} tasks across RQ queues.")
        return total_tasks > 0