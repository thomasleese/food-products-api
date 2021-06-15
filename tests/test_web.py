from fastapi.testclient import TestClient
import responses

from food_products_api.cache import Product
from food_products_api.web import app, cache


client = TestClient(app)


@responses.activate
def test_read_product():
    responses.add(
        responses.GET,
        "https://world-en.openfoodfacts.org/api/v0/product/abc.json",
        json={
            "product": {
                "code": "abc",
                "product_name": "ABC",
                "quantity": "100g",
                "brands_tags": ["brand"],
                "brands": "Brand",
                "serving_size": "50g",
                "nutriments": {
                    "energy_100g": 10,
                    "fat_100g": 10,
                    "saturated-fat_100g": 10,
                    "carbohydrates_100g": 10,
                    "fiber_100g": 10,
                    "sugars_100g": 10,
                    "proteins_100g": 10,
                    "energy_serving": 10,
                    "fat_serving": 10,
                    "saturated-fat_serving": 10,
                    "carbohydrates_serving": 10,
                    "fiber_serving": 10,
                    "sugars_serving": 10,
                    "proteins_serving": 10,
                },
            }
        },
    )

    product = Product("abc")
    del cache[product]

    response = client.get("/abc")
    assert response.status_code == 200

    response = client.get("/abc")
    assert response.status_code == 200
