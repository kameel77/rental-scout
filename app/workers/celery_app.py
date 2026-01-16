import os

from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery("rental_scout", broker=REDIS_URL, backend=REDIS_URL)
celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"
celery_app.conf.accept_content = ["json"]
celery_app.conf.task_track_started = True
celery_app.conf.worker_prefetch_multiplier = 1
celery_app.conf.task_always_eager = os.getenv("CELERY_ALWAYS_EAGER", "false").lower() == "true"
