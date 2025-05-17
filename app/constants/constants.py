from enum import Enum
from typing import List

class Constants:
    TASK_STATUS = {
        'PENDING': 'pending',
        'RUNNING': 'running',
        'COMPLETED': 'completed',
        'FAILED': 'failed'
    }
    
class ExecutionContext(Enum):
    CPU_BOUND = 'cpu_bound'
    IO_BOUND = 'io_bound'
    MEMORY_BOUND = 'memory_bound'
    NETWORK_BOUND = 'network_bound'

    @classmethod
    def get_available_execution_context(cls) -> List:
        return [
            cls.CPU_BOUND.value,
            cls.IO_BOUND.value,
            cls.MEMORY_BOUND.value,
            cls.NETWORK_BOUND.value    
        ]

class PriorityLevels(Enum):
    P0 = 'p0'
    P1 = 'p1'
    P2 = 'p2'
    
    @classmethod
    def get_priority_levels(cls) -> List:
        return [
            cls.P0.value,
            cls.P1.value,
            cls.P2.value
        ]
