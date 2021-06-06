class Serializer:
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
        return {
            "energy": data[f"energy_{suffix}"],
            "fat": data[f"fat_{suffix}"],
            "saturated_fat": data[f"saturated-fat_{suffix}"],
            "cholesterol": data.get(f"cholesterol_{suffix}"),
            "carbohydrates": data[f"carbohydrates_{suffix}"],
            "fiber": data[f"fiber_{suffix}"],
            "sugar": data[f"sugars_{suffix}"],
            "protein": data[f"proteins_{suffix}"],
            "calcium": data.get(f"calcium_{suffix}"),
            "iron": data.get(f"iron_{suffix}"),
            "potassium": data.get(f"potassium_{suffix}"),
            "sodium": data.get(f"sodium_{suffix}"),
            "vitamin_a": data.get(f"vitamin-a_{suffix}"),
            "vitamin_c": data.get(f"vitamin-c_{suffix}"),
            "vitamin_d": data.get(f"vitamin-d_{suffix}"),
        }

    @property
    def nutrition_data(self):
        return {
            "serving_size": self.product["serving_size"],
            "per_100g": self.build_nutrition_data(self.product["nutriments"], "100g"),
            "per_serving": self.build_nutrition_data(self.product["nutriments"], "serving"),
        }
