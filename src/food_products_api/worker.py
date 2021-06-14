import os

import celery


app = celery.Celery("food_products_api.worker")


app.conf.update(
    BROKER_URL=os.environ["REDIS_URL"],
    CELERY_RESULT_BACKEND=os.environ["REDIS_URL"],
    CELERY_TASK_SERIALIZER="json",
)
