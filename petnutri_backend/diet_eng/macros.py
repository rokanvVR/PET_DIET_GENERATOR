def calculate_macros(daily_cal, pet_data):

    protein_target = (daily_cal * pet_data["protein_percent"] / 100) / 4
    fat_target = (daily_cal * pet_data["fat_percent"] / 100) / 9
    carb_target = (daily_cal - protein_target*4 - fat_target*9) / 4

    return {
        "protein": protein_target,
        "fat": fat_target,
        "carbs": carb_target
    }