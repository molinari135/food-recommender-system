import random
import pandas as pd
from food_recommender_system.profiler import UserProfiler
from food_recommender_system.recommender import get_similar_food
from food_recommender_system.dataloader import DataLoader
from pathlib import Path
import time

from config import EXCLUDED_CATEGORIES, MEAL_GENERATION_CATEGORIES


def generate_meal(preferences_df: pd.DataFrame, filtered_df: pd.DataFrame, category: str):
    """
    Parameters:
    preferences_df (pd.DataFrame): DataFrame containing user preferences with columns "Category Name" and "Food Name".
    filtered_df (pd.DataFrame): DataFrame containing filtered food items for recommendation.
    category (str): The specific food category to include in the meal.
    Returns:
    tuple: A tuple containing two lists:
        - meal (list): A list of selected food items based on user preferences.
        - similar_meal (list): A list of similar food items for each item in the meal.
    """

    meal = []
    meal.extend([
        random.choice(
            preferences_df[preferences_df["Category Name"].isin(["Grains", "Gluten-Free Grains"])]["Food Name"].to_list()
        ),
        random.choice(preferences_df[preferences_df["Category Name"] == category]["Food Name"].to_list()),
        random.choice(preferences_df[preferences_df["Category Name"] == "Oils"]["Food Name"].to_list()),
        random.choice(preferences_df[preferences_df["Category Name"] == "Sauces"]["Food Name"].to_list()),
        random.choice(preferences_df[preferences_df["Category Name"] == "Vegetables"]["Food Name"].to_list()),
        random.choice(preferences_df[preferences_df["Category Name"] == "Fruits"]["Food Name"].to_list())
    ])

    # Find similar foods for each item in the meal
    similar_meal = []
    for food in meal:
        item_category = preferences_df[preferences_df["Food Name"] == food]["Category Name"].values[0]

        if item_category != ["Oils"]:
            similar_foods = get_similar_food(
                filtered_df, food_name=food, same_category=True, low_density_food=True
            )
            similar_meal.append(similar_foods[0][0])
        else:
            similar_meal.append(food)

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
        similar_foods = get_similar_food(
            filtered_df, food_name=item, same_category=True, low_density_food=True
        )
        similar_breakfast.append(similar_foods[0][0] if similar_foods else item)

    return breakfast, similar_breakfast


def generate_snack(preferences_df: pd.DataFrame, filtered_df: pd.DataFrame):
    """
    Generate a snack based on user preferences and filtered data.
    This function selects a snack consisting of three items from the user's preferences:
    - One item from the "Baked Products Breakfast" category.
    - One item from either the "Sweets Breakfast" or "Nuts Breakfast" category.
    - One item from the "Fruits" category.
    It then finds similar foods for each selected item from the filtered data, ensuring they are from the same category and are low-density foods.
    Args:
        preferences_df (pd.DataFrame): DataFrame containing user preferences with columns "Category Name" and "Food Name".
        filtered_df (pd.DataFrame): DataFrame containing filtered food data for finding similar foods.
    Returns:
        tuple: A tuple containing two lists:
            - snack (list): List of selected snack items.
            - similar_snack (list): List of similar snack items found in the filtered data.
    """

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
        similar_foods = get_similar_food(
            filtered_df, food_name=item, same_category=True, low_density_food=True
        )
        similar_snack.append(similar_foods[0][0] if similar_foods else item)

    return snack, similar_snack


def compute_meal_calories(meal: list, df: pd.DataFrame, servings: pd.DataFrame, verbose: bool = False) -> float:
    """
    Computes the total calories for a given meal.
    Args:
        meal (list): A list of food names included in the meal.
        df (pd.DataFrame): A DataFrame containing nutritional information for various foods.
        servings (pd.DataFrame): A DataFrame containing serving size information for different food categories.
        verbose (bool, optional): If True, prints detailed information about each food's calorie content. Defaults to False.
    Returns:
        float: The total calorie content of the meal.
    """

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
    """
    Generates a weekly meal plan based on user preferences, seasonal preferences, and intolerances.
    Args:
        df (pd.DataFrame): DataFrame containing the food dataset.
        servings (dict): Dictionary containing the frequency of servings per week for each category.
        user_profiler (UserProfiler): UserProfiler object to get user preferences and intolerances.
        filename (Path): Path to save the generated meal plan.
    Returns:
        dict: A dictionary containing the generated meals for Breakfast, Snack, Lunch, and Dinner.
    """

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
        print(f"Generating 7-day meal plan{'.' * (i + 1)}", end="\r")
        time.sleep(0.5)

    print("\nMeal plan generation complete!")

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
    for category, info in servings_count.items():
        if category in categories:
            if not preferences_df[preferences_df["Category Name"] == category].empty:
                for _ in range(info['frequency_per_week']):
                    meal, similar_meal = generate_meal(preferences_df, filtered_df, category)
                    meals.append((meal, similar_meal))

    # Select 7 random lunches and 7 random dinners
    selected_lunches = random.sample(meals, 7)
    meals = [meal for meal in meals if meal not in selected_lunches]
    selected_dinners = random.sample(meals, 7)
    generated_meals["Lunch"] = selected_lunches
    generated_meals["Dinner"] = selected_dinners

    # Save meal plan to profile
    user_profiler.set_meals(generated_meals)
    user_profiler.save_profile(filename)

    print(f"Weekly meal plan saved to {filename}")

    return generated_meals
