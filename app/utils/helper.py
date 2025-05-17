from datetime import datetime

from app.constants import ExecutionContext, PriorityLevels, ResponseMessages
from app.exceptions import BadRequestException
from app.utils import logger


class Helper:

    @staticmethod
    def validate_and_update_priority_group_data(priority_groups: dict, total_tasks: int):
        percentage_count = 0
        
        for key, value in priority_groups.items():
            if key not in PriorityLevels.get_priority_levels():
                raise BadRequestException(ResponseMessages.INVALID_PRIORITY_LEVEL.value)
            
            percentage_assigned = value.get('percentage', 0)
            execution_context = value.get('execution_context', '')
            
            if execution_context not in ExecutionContext.get_available_execution_context():
                raise BadRequestException(ResponseMessages.INVALID_EXECUTION_CONTEXT.value)
            
            if percentage_assigned > 100 or percentage_assigned <= 0:
                raise BadRequestException(ResponseMessages.INVALID_PERCENTAGE_VALUE.value)
            
            percentage_count += percentage_assigned
            tasks_count = (percentage_assigned / 100) * total_tasks
            value['count'] = int(tasks_count)
            
        if percentage_count != 100:
            raise BadRequestException(ResponseMessages.INVALID_PERCENTAGE_SUM.value)
        
        return priority_groups


    @staticmethod
    def get_current_time():
        return datetime.now()
