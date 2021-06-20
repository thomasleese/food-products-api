from decimal import Decimal
from typing import NamedTuple


class Serializer:
    class NutritionField(NamedTuple):
        input_name: str
        output_name: str
        units: str = "g"
        multiplier: Decimal = 1

    TO_MILLI = Decimal("0.001")

    NUTRITION_FIELDS = [
        NutritionField("energy", "energy", "kJ"),
        NutritionField("fat", "fat"),
        NutritionField("saturated_fat", "saturated-fat"),
        NutritionField("monounsaturated_fat", "monounsaturated-fat"),
        NutritionField("polyunsaturated_fat", "polyunsaturated-fat"),
        NutritionField("cholesterol", "cholesterol", "mg", TO_MILLI),
        NutritionField("carbohydrates", "carbohydrates"),
        NutritionField("fiber", "fiber", "mg", TO_MILLI),
        NutritionField("sugar", "sugars"),
        NutritionField("protein", "proteins"),
        NutritionField("calcium", "calcium", "mg", TO_MILLI),
        NutritionField("iron", "iron", "mg", TO_MILLI),
        NutritionField("potassium", "potassium", "mg", TO_MILLI),
        NutritionField("sodium", "sodium", "mg", TO_MILLI),
        NutritionField("vitamin_a", "vitamin-a", "mg", TO_MILLI),
        NutritionField("vitamin_c", "vitamin-c", "mg", TO_MILLI),
        NutritionField("vitamin_d", "vitamin-d", "mg", TO_MILLI),
    ]

    def __init__(self, open_food_facts_product):
        self.product = open_food_facts_product

    @property
    def data(self):
        return {
            "code": self.product["code"],
            "name": self.product["product_name"],
            "brand": self.brand_data,
            "quantity": self.product["quantity"],
            "nutrition": self.nutrition_data,
        }

    @property
    def brand_data(self):
        return {
            "slug": "-".join(self.product["brands_tags"]),
            "name": self.product["brands"],
        }

    @classmethod
    def build_nutrition_data(cls, data, suffix):
        output = {}

        for field in cls.NUTRITION_FIELDS:
            name = f"{field.output_name}_{field.units}"
            if str_value := data.get(f"{field.input_name}_{suffix}"):
                value = str(Decimal(str_value) * field.multiplier)
            else:
                value = None
            output[name] = value

        return output

    @property
    def nutrition_data(self):
        return {
            "serving_size": self.product["serving_size"],
            "per_100g": self.build_nutrition_data(self.product["nutriments"], "100g"),
            "per_serving": self.build_nutrition_data(
                self.product["nutriments"], "serving"
            ),
        }
