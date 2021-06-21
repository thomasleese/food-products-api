from decimal import Decimal
import re
from typing import NamedTuple


class Serializer:
    def __init__(self, open_food_facts_product):
        self.product = open_food_facts_product

    @property
    def data(self):
        return {
            "code": self.product["code"],
            "name": self.product["product_name"],
            "brand": self.brand_data,
            "servings": self.servings_data,
        }

    @property
    def brand_data(self):
        return {
            "slug": "-".join(self.product["brands_tags"]),
            "name": self.product["brands"],
        }

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

    SIZE_REGEX = re.compile(r"^(\d+)\s*(\w+)$")

    @classmethod
    def parse_size(cls, string):
        match = cls.SIZE_REGEX.match(string)
        return {
            "value": str(Decimal(match.group(1))),
            "units": match.group(2),
        }

    @property
    def servings_data(self):
        nutriments = self.product["nutriments"]
        serving_size = self.product["serving_size"]
        standard_size = "100" + ("ml" if "ml" in serving_size else "g")

        return [
            {
                "size": self.parse_size(serving_size),
                "nutrition": self.build_nutrition_data(nutriments, "serving"),
            },
            {
                "size": self.parse_size(standard_size),
                "nutrition": self.build_nutrition_data(nutriments, "100g"),
            },
        ]
