import random
import datetime
from recsys import DataLoader, RecommenderSystem
from profiler import UserProfiler, UserProfileWithIntolerances
import json

# Step 1: Load data using DataLoader
data_loader = DataLoader()
nutritional_data = data_loader.load_csv('nutritional-facts.csv')
servings_data = data_loader.load_json('food-servings.json')
seasonality_data = data_loader.load_json('food-seasonality.json')

# Step 3: Get the current month to filter seasonal foods
current_month = datetime.datetime.now().strftime('%B')

# Step 4: Function to get seasonal foods from the seasonality data
def get_seasonal_foods(category, food_to_category):
    seasonal_foods = seasonality_data["Italy"].get(current_month, [])
    return [food for food in food_to_category.get(category, []) if food in seasonal_foods]

def generate_meal(nutritional_data, servings_data):
    meal = {}

    # Map each food in the CSV to its category, including the new categories
    food_to_category = {
        category: nutritional_data[nutritional_data['Category Name'] == category]['Food Name'].tolist()
        for category in servings_data.keys() if category in nutritional_data['Category Name'].unique()
    }

    # Main dish: select from protein or grains
    main_options = ["Seafood", "White Meat", "Legumes", "Dairy", "Red Meat", "Lactose-Free Dairy", "Eggs"]
    main_choice = random.choice([opt for opt in main_options if servings_data[opt]["frequency_per_week"] > 0])
    food_choice = random.choice(food_to_category[main_choice])
    meal[main_choice] = {"food": food_choice, "serving_size": servings_data[main_choice]["serving_size"]}
    
    # Decrease the remaining frequency
    servings_data[main_choice]["frequency_per_week"] -= 1

    # Grains (including Gluten-Free Grains)
    grain_options = ["Grains", "Gluten-Free Grains"]
    for grain in grain_options:
        if servings_data[grain]["frequency_per_week"] > 0:
            food_choice = random.choice(food_to_category[grain])
            meal[grain] = {"food": food_choice, "serving_size": servings_data[grain]["serving_size"]}
            servings_data[grain]["frequency_per_week"] -= 1
        break

    # Vegetables (filter based on seasonality)
    if servings_data["Vegetables"]["frequency_per_week"] > 0:
        seasonal_vegetables = get_seasonal_foods("Vegetables", food_to_category)
        if seasonal_vegetables:
            food_choice = random.choice(seasonal_vegetables)
            meal["Vegetables"] = {"food": food_choice, "serving_size": servings_data["Vegetables"]["serving_size"]}
            servings_data["Vegetables"]["frequency_per_week"] -= 1

    # Fruits (filter based on seasonality)
    if servings_data["Fruits"]["frequency_per_week"] > 0:
        seasonal_fruits = get_seasonal_foods("Fruits", food_to_category)
        if seasonal_fruits:
            food_choice = random.choice(seasonal_fruits)
            meal["Fruits"] = {"food": food_choice, "serving_size": servings_data["Fruits"]["serving_size"]}
            servings_data["Fruits"]["frequency_per_week"] -= 1

    # Oils and Sauces (always included)
    meal["Oils and Sauces"] = {"food": "Olive oil", "serving_size": servings_data["Oils and Sauces"]["serving_size"]}

    return meal

# Step 7: User profiling and filtering based on preferences and intolerances
user_profiler = UserProfileWithIntolerances()

# Load existing users (for demonstration purposes)
user = user_profiler.get_user_by_id(user_id=1)
filtered_foods = user_profiler.filter_food_based_on_user_profile(user, nutritional_data)

def generate_week_of_meals(filtered_foods, servings_data):
    week_meals = {}

    # Generate meals for each day of the week (Monday to Sunday)
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        print(f"\nGenerating meals for {day}...")
        week_meals[day] = {
            "Lunch": generate_meal(filtered_foods, servings_data),
            "Dinner": generate_meal(filtered_foods, servings_data)
        }

    # Debugging: Print the frequency_per_week to check the remaining food options
    print("\nRemaining Frequency per Week:")
    for category, data in servings_data.items():
        print(f"{category}: {data['frequency_per_week']}")

    return week_meals

recommender = RecommenderSystem(nutritional_data, user_profiler.get_pantry("Italy"), seasonality_data, user)

# Generate the meals
full_week_meals = generate_week_of_meals(filtered_foods, servings_data)

def print_meals_with_recommendations(meals):
    print("\nFull Week of Meals with Recommended Ingredients:")

    for day, meal_data in meals.items():
        print(f"\n{day}:")

        # For each meal type (Lunch, Dinner)
        for meal_time, ingredients in meal_data.items():
            print(f"  {meal_time}:")
            for category, details in ingredients.items():
                print(f"    - {category}: {details['food']} ({details['serving_size']})")

                # Use recommender to find similar ingredients (based on the current ingredient)
                similar_ingredients = recommender.find_similar_ingredients([details['food']])

                # Display similar ingredients cleanly
                if similar_ingredients:
                    for ingredient, suggestions in similar_ingredients.items():
                        suggestion_list = ", ".join(suggestions)
                        print(f"      Suggested similar ingredient: {suggestion_list} (for variety or substitution)")
            print()

# Sample usage
print_meals_with_recommendations(full_week_meals)
