import json
import os
from typing import NamedTuple

import redis
import requests

from .serializer import Serializer


class Product(NamedTuple):
    code: str
    locale: str = "en"

    @property
    def cache_key(self):
        return f"product:{self.locale}:{self.code}"


class Cache:
    def __init__(self):
        self.redis = redis.Redis.from_url(os.environ["REDIS_URL"])

    def __getitem__(self, product):
        return json.loads(self.redis[product.cache_key])

    def __setitem__(self, product, data):
        self.redis[product.cache_key] = json.dumps(data)

    def save(self, product):
        url = f"https://world-{product.locale}.openfoodfacts.org/api/v0/product/{product.code}.json"
        headers = {
            "User-Agent": "Food Products API - https://github.com/orycion/food-products-api"
        }
        response = requests.get(url, headers=headers)
        data = Serializer(response.json()["product"]).data

        self[product] = data
        return data
