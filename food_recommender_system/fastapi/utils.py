import pandas as pd

MACRONUTRIENTS = ["Calories", "Carbs", "Fats", "Fiber", "Protein"]
MEAL_GENERATION_CATEGORIES = ["Seafood", "Lactose-Free Dairy", "Dairy", "Eggs", "Legumes", "White Meat", "Cured Meat", "Red Meat"]
EXCLUDED_CATEGORIES = ["Baby Foods", "Meals, Entrees, and Side Dishes", "Soups", "Spices", "Greens"]


def get_food_category(food_name: str, df: pd.DataFrame) -> str:
    food_info = df[df["Food Name"] == food_name]
    if not food_info.empty:
        return food_info["Category Name"].values[0]
    return None


def get_nutritional_info(food_name: str, df: pd.DataFrame, only_numbers: bool = True):
    food_info = df[df["Food Name"] == food_name]
    if not food_info.empty:
        return food_info.drop(columns=["Food Name", "Category Name"]) if only_numbers else food_info
    return None


def get_seasonal_foods(seasonality: dict, month: int):
    return seasonality.get(month, [])


def compute_energy_density(food_name: str, df: pd.DataFrame) -> int:
    food_info = get_nutritional_info(food_name, df)
    if food_info is not None:
        return food_info["Calories"].values[0] / 100
    return None
