from profiler import UserProfiler
from recommender import DataLoader, RecommenderSystem
from mealgen import generate_weekly_meal_plan
from justificator import Justificator
from datetime import datetime

# Paths to data files
PROFILE_FILE = "user_profile.json"
NUTRITIONAL_FACTS_PATH = "nutritional-facts.csv"
FOOD_SEASONALITY_PATH = "food-seasonality.json"


# Main process
def main():
    try:
        # Step 1: Load or create user profile
        profile_file = "user_profile.json"
        user_profiler = UserProfiler()
        user = user_profiler.load_profile(profile_file)

        dataloader = DataLoader()
        df = dataloader.load_csv("nutritional-facts.csv")
        seasonality = dataloader.load_json("food-seasonality.json")

        recommender = RecommenderSystem(
            df=df,
            seasonality=seasonality,
            user_profiler=user
        )

        justificator = Justificator()

        # intolerances = input("Are you lactose intolerant? (Yes/no)").strip().lower()
        
        # if intolerances == "yes":
        #     user.set_intolerances("Diary")

        # intolerances = input("Are you gluten intolerant? (Yes/no)").strip().lower()
        
        # if intolerances == "yes":
        #     user.set_intolerances("Gluten")
        
        # Save the profile
        user.save_profile()
        # recommender.ask_user_preferences()
        # recommender.ask_seasonal_preferences()

        # generate_weekly_meal_plan(user, dataloader, profile_file)

        today_day_of_week = datetime.now().weekday()

        today_lunch = user.get_meals()["Lunch"][today_day_of_week]
        today_dinner = user.get_meals()["Dinner"][today_day_of_week]

        print("Today's lunch is", today_lunch[0])
        print("Today's dinner is", today_dinner[0])

        print(justificator.compare_meals(today_lunch[0], today_lunch[1])[1])
        print(justificator.compare_meals(today_dinner[0], today_dinner[1])[1])

        print(justificator.recommend_fruit_or_vegetable(today_lunch[0][5]))
        print(justificator.recommend_fruit_or_vegetable(today_dinner[0][5]))

    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Run the main function
if __name__ == "__main__":
    main()
