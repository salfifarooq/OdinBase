import random
import time
from typing import Dict, Union

from celery import shared_task
from celery.result import AsyncResult

import app.core.celery as _


@shared_task(bind=True, max_retries=3)
def add(self, x: int, y: int) -> int:
    """Celery task to perform an addition with retry capability and simulated failure."""
    try:
        # simulate a long-running task
        time.sleep(5)
        # simulate a failure with a 60% chance
        if random.random() < 0.6:
            raise ValueError("simulated random failure")
        return x + y

    except Exception as exc:
        # retry the task with exponential backoff in case of failure
        countdown = 2**self.request.retries  # exp backoff
        raise self.retry(exc=exc, countdown=countdown)


class ExpensiveTaskService:
    """Service class for managing expensive Celery tasks."""

    @staticmethod
    def submit_add_task(x: int, y: int) -> str:
        """Submit an addition task to the Celery worker and return the task ID."""
        result = add.delay(x, y)
        return result.id

    @staticmethod
    def get_task_status(task_id: str) -> Dict[str, Union[str, int, None]]:
        """
        Retrieve the status and result of a task by its ID.

        Returns:
            A dictionary containing the task status and result.
            Raises ValueError if the task is not found.
        """
        task_result = AsyncResult(task_id)

        # check if the task has started
        if task_result.status == "PENDING":
            raise ValueError(f"task with id {task_id} not found")

        if task_result.failed():
            raise task_result.result

        return {
            "result": task_result.result if task_result.successful() else None,
            "status": task_result.status,
        }
