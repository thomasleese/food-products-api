web: gunicorn -k uvicorn.workers.UvicornWorker --pythonpath src food_products_api.web:app
worker: REMAP_SIGTERM=SIGQUIT celery worker --loglevel info --workdir src --app food_products_api.worker.app
