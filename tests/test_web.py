from fastapi.testclient import TestClient
import responses

from food_products_api.cache import Product
from food_products_api.web import app, cache


client = TestClient(app)


def test_read_product_no_bearer_token():
    response = client.get("/en/abc")
    assert response.status_code == 403


def test_read_product_invalid_bearer_token():
    response = client.get("/en/abc", headers={"Authorization": "Bearer invalid"})
    assert response.status_code == 401


@responses.activate
def test_read_product_not_found():
    responses.add(
        responses.GET,
        "https://world-en.openfoodfacts.org/api/v0/product/not-found.json",
        json={"code": "not-found", "status": 0, "status_verbose": "product not found"},
    )

    response = client.get("/en/not-found", headers={"Authorization": "Bearer test1"})
    assert response.status_code == 404


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

    response = client.get("/en/abc", headers={"Authorization": "Bearer test1"})
    assert response.status_code == 200

    response = client.get("/en/abc", headers={"Authorization": "Bearer test2"})
    assert response.status_code == 200
