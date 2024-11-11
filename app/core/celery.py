from celery import Celery
from celery.signals import after_task_publish

from app.core import config

celery = Celery(
    __name__,
    broker=config.CELERY_BROKER,
    backend=(
        config.CELERY_BACKEND
        if config.CELERY_BACKEND
        else f"db+postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASS}@{config.POSTGRES_HOST}/{config.POSTGRES_DB_NAME}"
    ),
)

celery.autodiscover_tasks(["app.apis.api_router.srv.expensive"])


# https://stackoverflow.com/questions/9824172/find-out-whether-celery-task-exists
@after_task_publish.connect
def update_sent_state(sender=None, headers=None, **kwargs):
    task = celery.tasks.get(sender)
    backend = task.backend if task else celery.backend
    backend.store_result(headers["id"], None, "SENT")
