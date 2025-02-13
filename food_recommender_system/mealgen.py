import random
import pandas as pd
from profiler import UserProfiler
from recommender import RecommenderSystem, DataLoader
from pathlib import Path
import time

from config import EXCLUDED_CATEGORIES, MEAL_GENERATION_CATEGORIES


def generate_meal(preferences_df: pd.DataFrame, filtered_df: pd.DataFrame):
    """
    Generate a meal based on user preferences and food categories.
    """

    meal = []
    meal.extend([
        random.choice(
            preferences_df[preferences_df["Category Name"].isin(["Grains", "Gluten-Free Grains"])]["Food Name"].to_list()
        ),
        random.choice(
            preferences_df[preferences_df["Category Name"].isin([
                "Legumes", "Dairy", "Lactose-Free Dairy", "Cured Meat", "Red Meat", "White Meat", "Seafood", "Eggs"
            ])]["Food Name"].to_list()
        ),
        random.choice(preferences_df[preferences_df["Category Name"] == "Oils"]["Food Name"].to_list()),
        random.choice(preferences_df[preferences_df["Category Name"] == "Sauces"]["Food Name"].to_list()),
        random.choice(preferences_df[preferences_df["Category Name"] == "Vegetables"]["Food Name"].to_list()),
        random.choice(preferences_df[preferences_df["Category Name"] == "Fruits"]["Food Name"].to_list())
    ])

    # Find similar foods for each item in the meal
    similar_meal = []
    for food in meal:
        item_category = preferences_df[preferences_df["Food Name"] == food]["Category Name"].values[0]

        if item_category not in ["Oils"]:
            similar_foods = RecommenderSystem.get_similar_food(
                filtered_df, food_name=food, same_category=True, low_density_food=True
            )
            similar_meal.append(similar_foods[0][0] if similar_foods else food)

    return meal, similar_meal


def generate_breakfast(preferences_df: pd.DataFrame, filtered_df: pd.DataFrame):
    breakfast = []

    breakfast.extend([
        random.choice(
            preferences_df[preferences_df["Category Name"] == "Dairy Breakfast"]["Food Name"].to_list()
            + preferences_df[preferences_df["Category Name"] == "Lactose-Free Dairy Breakfast"]["Food Name"].to_list()
            + preferences_df[preferences_df["Category Name"] == "Beverages"]["Food Name"].to_list()
        ),
        random.choice(preferences_df[preferences_df["Category Name"] == "Baked Products Breakfast"]["Food Name"].to_list()),
        random.choice(
            preferences_df[preferences_df["Category Name"] == "Sweets Breakfast"]["Food Name"].to_list()
            + preferences_df[preferences_df["Category Name"] == "Nuts Breakfast"]["Food Name"].to_list()
        ),
        random.choice(preferences_df[preferences_df["Category Name"] == "Fruits"]["Food Name"].to_list())
    ])

    similar_breakfast = []
    for item in breakfast:
        similar_foods = RecommenderSystem.get_similar_food(
            filtered_df, food_name=item, same_category=True, low_density_food=True
        )
        similar_breakfast.append(similar_foods[0][0] if similar_foods else item)

    return breakfast, similar_breakfast


def generate_snack(preferences_df: pd.DataFrame, filtered_df: pd.DataFrame):
    snack = []
    snack.extend([
        random.choice(preferences_df[preferences_df["Category Name"] == "Baked Products Breakfast"]["Food Name"].to_list()),
        random.choice(
            preferences_df[preferences_df["Category Name"] == "Sweets Breakfast"]["Food Name"].to_list()
            + preferences_df[preferences_df["Category Name"] == "Nuts Breakfast"]["Food Name"].to_list()
        ),
        random.choice(preferences_df[preferences_df["Category Name"] == "Fruits"]["Food Name"].to_list())
    ])

    similar_snack = []
    for item in snack:
        similar_foods = RecommenderSystem.get_similar_food(
            filtered_df, food_name=item, same_category=True, low_density_food=True
        )
        similar_snack.append(similar_foods[0][0] if similar_foods else item)

    return snack, similar_snack


def compute_meal_calories(meal: list, df: pd.DataFrame, servings: pd.DataFrame, verbose: bool = False) -> float:

    calories = 0

    for food_name in meal:
        food_info = DataLoader.get_nutritional_info(df, food_name, only_numbers=False)
        if food_info is not None:
            food_category = DataLoader.get_food_category(df, food_name)[0]
            serving_size = servings.get(food_category, {}).get('serving_size')
            food_calories = (food_info['Calories'].values[0] * serving_size) / 100
            if verbose:
                print(f"A serving size of {food_name} ({serving_size}g) has {int(food_calories)} kcal")
            calories += food_calories

    return calories


def generate_weekly_meal_plan(df: pd.DataFrame, servings: dict, user_profiler: UserProfiler, filename: Path):
    # Load user profile
    user_preferences = user_profiler.get_food_preferences()
    seasonal_preferences = user_profiler.get_seasonal_preferences()
    user_intolerances = user_profiler.get_intolerances()
    preferences = user_preferences + seasonal_preferences

    # Filter user preferences in the dataset
    preferences_df = df[df["Food Name"].isin(preferences)]

    if user_intolerances is not None:
        filtered_df = DataLoader.filter_categories(df, EXCLUDED_CATEGORIES + user_intolerances)
    else:
        filtered_df = DataLoader.filter_categories(df, EXCLUDED_CATEGORIES)

    seasonal_foods = df[df["Food Name"].isin(seasonal_preferences)]
    filtered_df = pd.concat([filtered_df, seasonal_foods])

    servings_count = servings.copy()
    generated_meals = {"Breakfast": [], "Snack": [], "Lunch": [], "Dinner": []}

    for i in range(3):
        print("Generating 7-day meal plan" + "." * (i + 1), end="\r")
        time.sleep(0.5)

    # Generate 7 breakfasts and snacks
    for _ in range(7):
        breakfast, similar_breakfast = generate_breakfast(preferences_df, filtered_df)
        snack, similar_snack = generate_snack(preferences_df, filtered_df)
        generated_meals["Breakfast"].append((breakfast, similar_breakfast))
        generated_meals["Snack"].append((snack, similar_snack))

    # Categories for meal generation
    categories = MEAL_GENERATION_CATEGORIES
    meals = []

    # Generate meals based on frequency_per_week
    for category in categories:
        if category in servings_count:
            info = servings_count[category]
            if not preferences_df[preferences_df["Category Name"] == category].empty:
                for _ in range(info["frequency_per_week"]):
                    meal, similar_meal = generate_meal(preferences_df, filtered_df)
                    meals.append((meal, similar_meal))

    # Select 7 random lunches and 7 random dinners
    selected_lunches = random.sample(meals, 7)
    selected_dinners = random.sample(meals, 7)
    generated_meals["Lunch"] = selected_lunches
    generated_meals["Dinner"] = selected_dinners

    # Save meal plan to profile
    user_profiler.set_meals(generated_meals)
    user_profiler.save_profile(filename)

    return generated_meals
