from dotenv import load_dotenv
load_dotenv()
import time
import os
from celery import Celery
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

celery_broker_url = f"{os.getenv('CELERY_BROKER_PROTOCOL')}://{os.getenv('CELERY_BROKER_USERNAME')}:{os.getenv('CELERY_BROKER_PASSWORD')}@{os.getenv('CELERY_BROKER_HOST')}"
logger.info(f"celery_broker_url: {celery_broker_url}")
logger.info(f"celery_backend_url: {os.getenv('CELERY_BACKEND_URL')}")

cfg = {
    "broker_url": celery_broker_url,
    "task_serializer": "json",
    "result_serializer": "json",
    "accept_content": ["json"],
    "worker_prefetch_multiplier": 1,
    "task_acks_late": False,
    "task_track_started": True,
    "result_expires": 604800,  # one week
    "task_reject_on_worker_lost": True,
    "task_queue_max_priority": 10,
    "enable_utc": True,
    "broker_connection_retry_on_startup": True,
    "worker_cancel_long_running_tasks_on_connection_loss": True,
}

celery_app = Celery(
    __name__,
    broker=celery_broker_url,
    backend=os.getenv('CELERY_RESULT_BACKEND'),
    task_queue_max_priority=10,
    kwargs=cfg,
)

@celery_app.task(name="print_task")
def print_task(msg):
    time.sleep(5)
    print(msg)
    return msg
