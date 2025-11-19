from celery import Celery
from backend.app.config import settings

celery = Celery(
    "product_importer",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery.autodiscover_tasks(["backend.app.tasks"])
