web: gunicorn -k uvicorn.workers.UvicornWorker --pythonpath src food_products_api.web:app
worker: REMAP_SIGTERM=SIGQUIT celery --workdir src worker --loglevel info --app food_products_api.worker.app
