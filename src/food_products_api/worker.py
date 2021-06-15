import os

import celery

from .cache import Cache, Product


app = celery.Celery("food_products_api.worker")
cache = Cache()


app.conf.update(
    broker_url=os.environ["REDIS_URL"],
    result_backend=os.environ["REDIS_URL"],
    task_serializer="json",
)


@app.task
def cache_save(code, locale):
    product = Product(code, locale)
    cache.save(product)
