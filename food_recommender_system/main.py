from profiler import UserProfiler
from recommender import DataLoader, RecommenderSystem
from mealgen import generate_weekly_meal_plan
from justificator import Justificator
from datetime import datetime
from moodmod import change_meal
import os

# Paths to data files
PROFILE_FILE = "user_profile.json"
NUTRITIONAL_FACTS_PATH = "nutritional-facts.csv"
FOOD_SEASONALITY_PATH = "food-seasonality.json"


# Main process
def main():
    try:
        # Step 1: Load or create user profile
        name = input("Please, enter name_surname to create or load your profile: ").strip().lower()
        profile_file = f"{name}.json"

        user_profiler = UserProfiler()

        if not os.path.exists(profile_file):
            print(f"Profile '{profile_file}' not found. Creating a new profile...")
            user_profiler.create_new_profile(profile_file)  # Create the profile

        user = user_profiler.load_profile(profile_file)

        dataloader = DataLoader()
        df = dataloader.load_csv("nutritional-facts.csv")
        seasonality = dataloader.load_json("food-seasonality.json")
        servings = dataloader.load_json("food-servings.json")
        fast_food_equiv = dataloader.load_json("fast-food-equiv.json")

        recommender = RecommenderSystem(
            df=df,
            seasonality=seasonality,
            user_profiler=user
        )

        justificator = Justificator()

        if user.get_meals() == {} and user.get_intolerances() == []:

            intolerances = input("Are you lactose intolerant? (Yes/no)").strip().lower()
            if intolerances == "yes":
                user.set_intolerances("Lactose")

            intolerances = input("Are you gluten intolerant? (Yes/no)").strip().lower()
            if intolerances == "yes":
                user.set_intolerances("Gluten")

            # Save the profile
            user.save_profile(profile_file)
            recommender.ask_user_preferences()
            recommender.ask_seasonal_preferences()

            generate_weekly_meal_plan(user, dataloader, profile_file)

        today_day_of_week = datetime.now().weekday()

        if today_day_of_week == 0:
            user.set_used_jolly(False)

        current_hour = datetime.now().hour

        meal = ""

        if 24 <= current_hour < 9:
            meal = "Breakfast"
        if 9 <= current_hour < 11:
            meal = "Snack"
        if 11 <= current_hour < 14:
            meal = "Lunch"
        if 14 <= current_hour < 17:
            meal = "Snack"
        if 17 <= current_hour < 24:
            meal = "Dinner"

        current_meal = user.get_meals()[meal][today_day_of_week][0]
        current_alternative = user.get_meals()[meal][today_day_of_week][1]

        justificate = True

        print(f"Today's {meal} is:")
        for food in current_meal:
            category = DataLoader.find_food_category(df, food)[0]
            if category != "Fast Foods":
                serving = servings.get(category, {}).get('serving_size')
                print(f"- {serving}g of {food}")
            else:
                print(food)
                justificate = False

        print("\nAlternatively, you can have:")
        for food in current_alternative:
            category = DataLoader.find_food_category(df, food)
            if category.size > 0:
                serving = servings.get(category[0], {}).get('serving_size')
                print(f"- {serving}g of {food}")
            else:
                print(food)
                justificate = False
        if justificate:
            print("\n", justificator.compare_meals(current_meal, current_alternative)[0])
            print("\n", justificator.compare_meals(current_meal, current_alternative)[1])
            print("\n", justificator.recommend_seasonal(current_meal[len(current_meal) - 1]))
            print("\n", justificator.recommend_seasonal(current_alternative[len(current_alternative) - 1]))

        if meal in ["Lunch", "Dinner"]:
            if user.get_used_jolly():
                print("You have used your jolly for this week, you have to wait for the next one!")
            else:
                change_meal(user, df, fast_food_equiv, meal)
                user.set_used_jolly(True)
                user.save_profile(profile_file)

    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Run the main function
if __name__ == "__main__":
    main()
