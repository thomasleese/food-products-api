from fastapi import FastAPI

from .cache import Cache, Product
from .worker import cache_save


app = FastAPI()
cache = Cache()


@app.get("/{code}")
def read_product(code: str):
    product = Product(code)

    try:
        response = cache[product]
        cache_save.delay(product.code, product.locale)
    except KeyError:
        response = cache.save(product)

    return response
