import random
import pandas as pd
from profiler import UserProfiler
from recommender import RecommenderSystem, DataLoader

EXCLUDED_CATEGORIES = [
    "Baby Foods", "Meals, Entrees, and Side Dishes", "Soups", "Spices", "Fruits", "Vegetables", "Greens"
]


def generate_meal(user_preferences: pd.DataFrame, df: pd.DataFrame):
    """
    Generate a meal based on user preferences and food categories.
    """

    meal = []
    meal.extend([
        random.choice(
            user_preferences[user_preferences["Category Name"].isin(["Grains", "Gluten-Free Grains"])]
            ["Food Name"].to_list()
        ),
        random.choice(
            user_preferences[user_preferences["Category Name"].isin([
                "Legumes", "Dairy", "Lactose-Free Dairy", "Cured Meat", "Red Meat", "White Meat", "Seafood", "Eggs"
            ])]["Food Name"].to_list()
        ),
        random.choice(user_preferences[user_preferences["Category Name"] == "Oils"]["Food Name"].to_list()),
        random.choice(user_preferences[user_preferences["Category Name"] == "Sauces"]["Food Name"].to_list()),
        random.choice(user_preferences[user_preferences["Category Name"] == "Vegetables"]["Food Name"].to_list()),
        random.choice(user_preferences[user_preferences["Category Name"] == "Fruits"]["Food Name"].to_list())
    ])

    # Find similar foods for each item in the meal
    similar_meal = []
    for item in meal:
        item_category = user_preferences[user_preferences["Food Name"] == item]["Category Name"].values[0]

        if item_category not in ["Oils", "Vegetables"]:
            similar_foods = RecommenderSystem.find_similar_food(df, food_name=item, n=1, same_category=True, low_density_food=True)
            similar_meal.append(similar_foods[0][0] if similar_foods else item)
        else:
            similar_meal.append(item)

    return meal, similar_meal


def generate_breakfast(user_preferences: pd.DataFrame, df: pd.DataFrame):
    breakfast = []
    breakfast.extend([
        random.choice(
            df[df["Category Name"] == "Dairy Breakfast"]["Food Name"].to_list() +
            df[df["Category Name"] == "Lactose-Free Dairy Breakfast"]["Food Name"].to_list() +
            df[df["Category Name"] == "Beverages"]["Food Name"].to_list()
        ),
        random.choice(df[df["Category Name"] == "Baked Products Breakfast"]["Food Name"].to_list()),
        random.choice(
            df[df["Category Name"] == "Sweets Breakfast"]["Food Name"].to_list() +
            df[df["Category Name"] == "Nuts Breakfast"]["Food Name"].to_list()
        ),
        random.choice(df[df["Category Name"] == "Fruits"]["Food Name"].to_list())
    ])

    similar_breakfast = []
    for item in breakfast:
        similar_foods = RecommenderSystem.find_similar_food(df, food_name=item, n=1, same_category=True, low_density_food=True)
        similar_breakfast.append(similar_foods[0][0] if similar_foods else item)

    return breakfast, similar_breakfast


def generate_snack(user_preferences: pd.DataFrame, df: pd.DataFrame):
    snack = []
    snack.extend([
        random.choice(df[df["Category Name"] == "Baked Products Breakfast"]["Food Name"].to_list()),
        random.choice(
            df[df["Category Name"] == "Sweets Breakfast"]["Food Name"].to_list() +
            df[df["Category Name"] == "Nuts Breakfast"]["Food Name"].to_list()
        ),
        random.choice(df[df["Category Name"] == "Fruits"]["Food Name"].to_list())
    ])

    similar_snack = []
    for item in snack:
        similar_foods = RecommenderSystem.find_similar_food(df, food_name=item, n=1, same_category=True, low_density_food=True)
        similar_snack.append(similar_foods[0][0] if similar_foods else item)

    return snack, similar_snack


def compute_meal_calories(meal: list, df: pd.DataFrame, servings: pd.DataFrame, verbose: bool = False):
    """
    Computes the total calorie content for a given meal.

    Parameters:
    - meal: list of food items (str)
    - df: DataFrame containing food nutritional information
    - servings: Dictionary mapping food categories to serving sizes
    - verbose: Boolean value to print more info

    Returns:
    - Total calories for the meal
    """
    calories = 0

    for food in meal:
        food_info = DataLoader.find_nutritional_info(df, food, only_numbers=False)
        if food_info is not None:
            food_category = food_info['Category Name'].values[0]
            serving_size = servings.get(food_category, {}).get('serving_size')
            food_calories = (food_info['Calories'].values[0] * serving_size) / 100
            if verbose:
                print(f"A serving size of {food} ({serving_size}g) has {int(food_calories)} kcal")
            calories += food_calories

    return calories


if __name__ == "__main__":
    user_profiler = UserProfiler.load_profile("user_profile.json")

    user_preferences = user_profiler.get_food_preferences()
    seasonal_preferences = user_profiler.get_seasonal_preferences()
    user_intolerances = user_profiler.get_intolerances()
    preferences = user_preferences + seasonal_preferences

    dataloader = DataLoader()
    df = dataloader.load_csv("nutritional-facts.csv")
    servings = dataloader.load_json("food-servings.json")

    user_preferences_df = df[df["Food Name"].isin(preferences)]
    filtered_df = DataLoader.filter_categories(df, EXCLUDED_CATEGORIES)
    seasonal_foods = df[df["Food Name"].isin(seasonal_preferences)]
    filtered_df = pd.concat([filtered_df, seasonal_foods])

    servings_count = servings.copy()

    generated_meals = {"Breakfast": [], "Snack": [], "Lunch": [], "Dinner": []}

    for _ in range(7):  # Loop 7 times to generate 7 breakfasts
        breakfast, similar_breakfast = generate_breakfast(user_preferences_df, filtered_df)
        snack, similar_snack = generate_snack(user_preferences_df, filtered_df)
        generated_meals["Breakfast"].append((breakfast, similar_breakfast))
        generated_meals["Snack"].append((snack, similar_snack))

        # Categories for which meals need to be generated
    categories = ["Seafood", "Lactose-Free Dairy", "Dairy", "Eggs", "Legumes", "White Meat", "Cured Meat", "Red Meat"]

    meals = []

    # Generate meals based on frequency_per_week for each category
    for category in categories:
        if category in servings_count:
            info = servings_count[category]
            # Check if category is available in user preferences
            if not user_preferences_df[user_preferences_df["Category Name"] == category].empty:
                for _ in range(info["frequency_per_week"]):
                    # Generate a meal for each category
                    if category == "Seafood":
                        meal, similar_meal = generate_meal(user_preferences_df, filtered_df)  # Replace with the actual function
                    elif category == "Lactose-Free Dairy":
                        meal, similar_meal = generate_meal(user_preferences_df, filtered_df)
                    elif category == "Dairy":
                        meal, similar_meal = generate_meal(user_preferences_df, filtered_df)
                    elif category == "Eggs":
                        meal, similar_meal = generate_meal(user_preferences_df, filtered_df)
                    elif category == "Legumes":
                        meal, similar_meal = generate_meal(user_preferences_df, filtered_df)
                    elif category == "White Meat":
                        meal, similar_meal = generate_meal(user_preferences_df, filtered_df)
                    elif category == "Cured Meat":
                        meal, similar_meal = generate_meal(user_preferences_df, filtered_df)
                    elif category == "Red Meat":
                        meal, similar_meal = generate_meal(user_preferences_df, filtered_df)

                    # Add the generated meals to the generated meals dictionary
                    meals.append((meal, similar_meal))

    # Randomly select 7 lunches and 7 dinners from the candidates
    selected_lunches = random.sample(meals, 7)
    selected_dinners = random.sample(meals, 7)

    # Store the selected meals in the generated_meals dictionary
    generated_meals["Lunch"] = selected_lunches
    generated_meals["Dinner"] = selected_dinners

    user_profiler.set_meals(generated_meals)
    user_profiler.save_profile("user_profile.json")

    # meal, similar_meal = generate_meal(user_preferences_df, filtered_df)
    # breakfast, similar_breakfast = generate_breakfast(user_preferences_df, filtered_df)
    # snack, similar_snack = generate_snack(user_preferences_df, filtered_df)

    # calories1 = compute_meal_calories(meal, filtered_df, servings)
    # print("Generated Meal:", meal)
    # print(f"This meal has {int(calories1)} kcal")

    # calories2 = compute_meal_calories(similar_meal, filtered_df, servings)
    # print("Alternative Meal:", similar_meal)
    # print(f"This meal has {int(calories2)} kcal")

    # calories3 = compute_meal_calories(breakfast, filtered_df, servings)
    # print("Alternative Meal:", breakfast)
    # print(f"This meal has {int(calories3)} kcal")

    # calories4 = compute_meal_calories(similar_breakfast, filtered_df, servings)
    # print("Alternative Meal:", similar_breakfast)
    # print(f"This meal has {int(calories4)} kcal")

    # calories5 = compute_meal_calories(snack, filtered_df, servings)
    # print("Alternative Meal:", snack)
    # print(f"This meal has {int(calories4)} kcal")

    # calories6 = compute_meal_calories(similar_snack, filtered_df, servings)
    # print("Alternative Meal:", similar_snack)
    # print(f"This meal has {int(calories4)} kcal")
