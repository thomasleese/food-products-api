import pytest

from food_products_api.serializer import Serializer


def test_product_with_all_fields():
    product = {
        "code": 123,
        "product_name": "Product Name",
        "brands_tags": ["brand"],
        "brands": "Brand",
        "quantity": "50g",
        "serving_size": "25g",
        "nutriments": {
            "energy_serving": 10,
            "energy_100g": 10,
            "fat_serving": 10,
            "fat_100g": 10,
            "saturated-fat_serving": 10,
            "saturated-fat_100g": 10,
            "carbohydrates_serving": 10,
            "carbohydrates_100g": 10,
            "fiber_serving": 10,
            "fiber_100g": 10,
            "sugars_serving": 10,
            "sugars_100g": 10,
            "proteins_serving": 10,
            "proteins_100g": 10,
        },
    }

    serialization = Serializer(product).data

    assert serialization["name"] == "Product Name"


@pytest.mark.parametrize(
    "input,output_value,output_units", [("100g", "100", "g"), ("50 ml", "50", "ml")]
)
def test_parse_size(input, output_value, output_units):
    assert Serializer.parse_size(input) == {
        "value": output_value,
        "units": output_units,
    }
