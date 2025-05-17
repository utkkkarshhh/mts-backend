from pydantic import BaseModel

class PriorityModel(BaseModel):
    percentage: int
    execution_context: str

class PrioritiesModel(BaseModel):
    p0: PriorityModel
    p1: PriorityModel
    p2: PriorityModel

class TasksModel(BaseModel):
    total_count: int
    priorities: PrioritiesModel

class TaskRequest(BaseModel):
    tasks: TasksModel
