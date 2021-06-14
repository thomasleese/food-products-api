import os

import celery


app = celery.Celery("food_products_api.worker")


app.conf.update(
    broker_url=os.environ["REDIS_URL"],
    result_backend=os.environ["REDIS_URL"],
    task_serializer="json",
)
