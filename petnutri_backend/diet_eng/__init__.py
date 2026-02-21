from .calories import calculate_daily_calories
from .macros import calculate_macros
from .planner import generate_weekly_plan
from .pricing import calculate_cost

def generate_meal_plan(user):

    daily_cal, pet_data = calculate_daily_calories(user)
    macros = calculate_macros(daily_cal, pet_data)

    weekly_plan, weekly_totals, grocery = generate_weekly_plan(
        user, daily_cal, macros
    )

    monthly_grocery, total_cost = calculate_cost(grocery)

    return {
        "weekly_plan": weekly_plan,
        "weekly_totals": weekly_totals,
        "monthly_grocery": monthly_grocery,
        "monthly_cost": total_cost
    }