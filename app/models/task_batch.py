from tortoise import fields, models
import uuid
from typing import Optional

class TaskBatch(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    total_count = fields.IntField()
    priority_config = fields.JSONField()
    status = fields.CharField(max_length=20, default="PENDING")
    success_count = fields.IntField(default=0)
    failure_count = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)
    completed_at = fields.DatetimeField(null=True)

    class Meta:
        table = "task_batches"
