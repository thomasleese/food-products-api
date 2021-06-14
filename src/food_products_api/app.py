import asyncio

from fastapi import FastAPI
import requests

from .serializer import Serializer


app = FastAPI()


@app.get("/{code}")
async def read_product(code: str):
    url = f"https://world.openfoodfacts.org/api/v0/product/{code}.json"
    headers = {
        "User-Agent": "Food Products API - https://github.com/orycion/food-products-api"
    }
    response = await asyncio.to_thread(requests.get, url, headers=headers)
    data = response.json()

    return Serializer(data["product"]).data
