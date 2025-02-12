import datetime
import random
from profiler import UserProfiler
from recommender import DataLoader


def load_user_profile(profile_file):
    """Load user profile from JSON file."""
    return UserProfiler.load_profile(profile_file)


def load_data():
    """Load necessary data for the meal suggestion process."""
    dataloader = DataLoader()
    df = dataloader.load_csv("nutritional-facts.csv")
    fast_food_equiv = dataloader.load_json("fast-food-equiv.json")
    return df, fast_food_equiv


def change_meal(user_profiler, df, fast_food_equiv, meal_name):
    """Suggest a new meal based on user mood and preferences."""
    today_day_of_week = datetime.datetime.now().weekday()
    weekly_meals = user_profiler.get_meals()

    is_happy = input("Is today a happy day? (yes/no): ").strip().lower() == 'yes'

    if not is_happy:
        user_preferences_df = df[df["Category Name"] == "Fast Foods"]

        if not user_preferences_df.empty:
            fast_food = random.choice(user_preferences_df["Food Name"].to_list())
            new_lunch = [[fast_food]]
            food_equivalents = fast_food_equiv.get(fast_food, [])

            if food_equivalents:
                new_lunch.append(food_equivalents)

            weekly_meals[meal_name][today_day_of_week] = new_lunch

            user_profiler.set_used_jolly(True)
            print(f"No worries! Your {meal_name} has been changed!")
            print(f"Today you can have a {", ".join(weekly_meals[meal_name][today_day_of_week][0])}")
            print(f"Alternatively, you can make a {", ".join(weekly_meals[meal_name][today_day_of_week][1])}")
        else:
            print("No fast food options available.")
    else:
        print(f"Happy day, no changes to your {meal_name}!")

    user_profiler.set_meals(weekly_meals)
    user_profiler.save_profile("user_profile.json")


def reset_jolly_if_new_week(user_profiler):
    """Reset the jolly flag if today is the first day of the week (Monday)."""
    today = datetime.datetime.now()

    # Check if today is Monday and if it's past midnight
    if today.weekday() == 0 and today.hour == 0 and today.minute == 0:
        user_profiler.set_used_jolly(False)
        print("Jolly has been reset for the new week.")


def check_jolly_usage(user_profiler):
    """Check if the 'jolly' has been used and alert the user."""
    if user_profiler.get_used_jolly():
        print("You have used your jolly for today! Enjoy your special meal!")
    else:
        print("You have not used your jolly today.")


def main():
    user_profiler = load_user_profile("user_profile.json")
    df, fast_food_equiv = load_data()

    # Suggest a new lunch if needed
    change_meal(user_profiler, df, fast_food_equiv, "Lunch")

    # Check if the jolly has been used
    check_jolly_usage(user_profiler)


if __name__ == "__main__":
    main()
