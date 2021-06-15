from unittest import mock

import responses


with mock.patch.dict("os.environ", {"REDIS_URL": "redis://localhost"}, clear=True):
    from food_products_api.worker import app, cache_save


def test_app():
    assert app


@responses.activate
def test_cache_save():
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

    cache_save("abc", "en")
