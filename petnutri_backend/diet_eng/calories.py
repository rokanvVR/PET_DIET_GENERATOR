import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_json(name):
    with open(os.path.join(BASE_DIR, "data", name)) as f:
        return json.load(f)

pet_models = load_json("pet_models.json")
breed_data = load_json("breed_data.json")
config = load_json("config.json")

def calculate_daily_calories(user):

    pet_data = pet_models[user["pet_type"]][user["age_group"]]

    rer = (user["weight"] * 30) + 70
    daily_cal = rer * pet_data["activity_multipliers"][user["activity_level"]]

    if user["breed"] in breed_data:
        daily_cal *= breed_data[user["breed"]]["energy_modifier"]

    for condition in user["health_conditions"]:
        if condition in config["health_modifiers"]:
            daily_cal *= config["health_modifiers"][condition]

    return daily_cal, pet_data