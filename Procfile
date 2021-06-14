web: gunicorn -k uvicorn.workers.UvicornWorker --pythonpath src food_products_api.web:app
worker: celery worker --workdir src --app=food_products_api.worker.app
