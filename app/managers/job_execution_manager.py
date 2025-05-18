from app.utils import logger

class JobExecutionManager:

    @staticmethod
    def process_task(task: dict):
        logger.info(f"Processing task {task['id']} with priority {task['priority']}")
        return

    @staticmethod
    def process_task_job(task: dict):
        JobExecutionManager.process_task(task)