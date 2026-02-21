import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_json(name):
    with open(os.path.join(BASE_DIR, "data", name)) as f:
        return json.load(f)

ingredients = load_json("ingredients.json")

def calculate_cost(grocery):

    monthly_grocery = {k:v*4 for k,v in grocery.items()}
    total_cost = 0

    for name, grams in monthly_grocery.items():
        ingredient = next((i for i in ingredients if i["name"] == name), None)

        if ingredient and "price_per_kg" in ingredient:
            kg = grams / 1000
            total_cost += kg * ingredient["price_per_kg"]

    return monthly_grocery, round(total_cost)