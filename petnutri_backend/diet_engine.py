import os
import json
import random
import itertools

import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "data", "pet_models.json")) as f:
    pet_models = json.load(f)

with open(os.path.join(BASE_DIR, "data", "breed_data.json")) as f:
    breed_data = json.load(f)

with open(os.path.join(BASE_DIR, "data", "allergy.json")) as f:
    allergy_map = json.load(f)

with open(os.path.join(BASE_DIR, "data", "ingredients.json")) as f:
    ingredients = json.load(f)


def generate_meal_plan(user):

    # ---------------- CALORIE CALCULATION ----------------
    pet_data = pet_models[user["pet_type"]][user["age_group"]]

    rer = (user["weight"] * 30) + 70
    daily_cal = rer * pet_data["activity_multipliers"][user["activity_level"]]

    # Breed modifier
    if user["breed"] in breed_data:
        daily_cal *= breed_data[user["breed"]]["energy_modifier"]

    # Health modifier
    if "obesity" in user["health_conditions"]:
        daily_cal *= 0.9

    # ---------------- MACRO TARGETS ----------------
    protein_target = (daily_cal * pet_data["protein_percent"] / 100) / 4
    fat_target = (daily_cal * pet_data["fat_percent"] / 100) / 9
    carb_target = (daily_cal - protein_target*4 - fat_target*9) / 4

    # ---------------- FILTERING ----------------
    banned = set()
    for allergy in user["allergies"]:
        if allergy in allergy_map:
            banned.update(allergy_map[allergy])

    filtered = [
        i for i in ingredients
        if i["name"] not in banned and
        not (user["diet_type"] == "veg" and i["type"] == "nonveg")
    ]

    protein_sources = [i for i in filtered if i["category"] == "protein"]
    carb_sources = [i for i in filtered if i["category"] == "carb"]
    veg_sources = [i for i in filtered if i["category"] == "vegetable"]

    if not protein_sources or not carb_sources:
        raise ValueError("Not enough ingredients after filtering.")

    random.shuffle(protein_sources)
    random.shuffle(carb_sources)

    # ---------------- MEAL SPLIT ----------------
    meal_split = {
        "Breakfast": 0.3,
        "Lunch": 0.35,
        "Dinner": 0.35
    }

    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    weekly_plan = {}
    weekly_totals = {"protein":0,"fat":0,"carbs":0,"calories":0}
    grocery = {}

    # ---------------- WEEKLY MEAL GENERATION ----------------
    for day_index, day in enumerate(days):
        weekly_plan[day] = {}

        for meal_index, meal in enumerate(meal_split):

            meal_cal_target = daily_cal * meal_split[meal]
            meal_protein_target = protein_target * meal_split[meal]
            meal_carb_target = carb_target * meal_split[meal]

            best_combo = None
            lowest_score = float("inf")

            for protein, carb in itertools.product(protein_sources, carb_sources):

                if protein["protein"] == 0 or carb["carbs"] == 0:
                    continue

                protein_g = (meal_protein_target / protein["protein"]) * 100
                carb_g = (meal_carb_target / carb["carbs"]) * 100

                if protein_g > 500 or carb_g > 500:
                    continue

                calories = (
                    (protein_g/100)*protein["calories"] +
                    (carb_g/100)*carb["calories"]
                )

                protein_actual = (protein_g/100)*protein["protein"]

                calorie_error = abs(calories - meal_cal_target)
                protein_error = abs(protein_actual - meal_protein_target)

                score = calorie_error + protein_error

                if score < lowest_score:
                    lowest_score = score
                    best_combo = (protein, carb, protein_g, carb_g, calories)

            if not best_combo:
                continue

            protein, carb, protein_g, carb_g, calories = best_combo

            veg = veg_sources[(day_index + meal_index) % len(veg_sources)]
            veg_g = 50

            meal_protein = (protein_g/100)*protein["protein"]
            meal_carbs = (carb_g/100)*carb["carbs"]
            meal_fat = (protein_g/100)*protein["fat"]

            weekly_totals["protein"] += meal_protein
            weekly_totals["carbs"] += meal_carbs
            weekly_totals["fat"] += meal_fat
            weekly_totals["calories"] += calories

            for item, grams in [(protein,protein_g),(carb,carb_g),(veg,veg_g)]:
                grocery[item["name"]] = grocery.get(item["name"],0) + grams

            weekly_plan[day][meal] = {
                "ingredients": {
                    "protein": {"name":protein["name"],"grams":round(protein_g,1)},
                    "carb": {"name":carb["name"],"grams":round(carb_g,1)},
                    "vegetable": {"name":veg["name"],"grams":veg_g}
                },
                "nutrients": {
                    "protein": round(meal_protein,1),
                    "carbs": round(meal_carbs,1),
                    "fat": round(meal_fat,1),
                    "calories": round(calories,1)
                }
            }

    # ---------------- MONTHLY CALCULATIONS ----------------
    monthly_totals = {k:v*4 for k,v in weekly_totals.items()}
    monthly_grocery = {k:v*4 for k,v in grocery.items()}

    # ---------------- COST CALCULATION ----------------
    total_cost = 0

    for name, grams in monthly_grocery.items():
        ingredient = next((i for i in ingredients if i["name"] == name), None)

        if ingredient and "price_per_kg" in ingredient:
            kg = grams / 1000
            total_cost += kg * ingredient["price_per_kg"]

    return {
        "weekly_plan": weekly_plan,
        "weekly_totals": weekly_totals,
        "monthly_totals": monthly_totals,
        "monthly_grocery": monthly_grocery,
        "monthly_cost": round(total_cost)
    }