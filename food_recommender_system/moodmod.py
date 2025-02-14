from datetime import datetime
from profiler import UserProfiler
from justificator import Justificator
from pathlib import Path
import pandas as pd
import random


def change_meal(user: UserProfiler, df: pd.DataFrame, meal_name: str, filename: Path):
    """
    Suggest a new meal based on user mood and preferences.
    Parameters:
    user (UserProfiler): The user profile containing meal preferences and mood information.
    df (pd.DataFrame): DataFrame containing food items and their categories.
    meal_name (str): The name of the meal to be changed (e.g., "Lunch", "Dinner").
    filename (Path): The path to the file where the user profile is saved.
    Returns:
    None
    """

    today_day_of_week = datetime.now().weekday()
    weekly_meals = user.get_meals()

    has_used_jolly = user.get_used_jolly()

    if has_used_jolly:
        print(f"Have a nice {meal_name.lower()}!")
    else:
        if meal_name == "Lunch" or meal_name == "Dinner":
            is_stressed = input("Are you feeling stressed today? (yes/no): ").strip().lower() == 'yes'

            if is_stressed:
                Justificator.get_current_meal(user)
                print("\n😉 Just for today, let's eat something that could improve your mood!")

                fast_foods = df[df["Category Name"] == "Fast Foods"]
                fast_food = random.choice(fast_foods["Food Name"].to_list())

                # Overwrite the fast food in the third position of the current meal
                if len(weekly_meals[meal_name][today_day_of_week]) >= 3:
                    weekly_meals[meal_name][today_day_of_week][2] = [fast_food]

                user.set_used_jolly(True)
                user.set_meals(weekly_meals)
                user.save_profile(filename)
                print(f"🍽️ Today you can have {fast_food}")

                user.set_meals(weekly_meals)
                user.save_profile(filename)
                print("🫡  Take care of yourself!")
        else:
            print(f"Have a nice {meal_name.lower()}!")


def reset_jolly_if_new_week(user: UserProfiler):
    """
    Reset the jolly flag if today is the first day of the week (Monday).
    This function checks if the current day is Monday and if the current time is exactly midnight.
    If both conditions are met, it resets the 'jolly' flag for the user to indicate that a new week has started.
    Args:
        user (UserProfiler): An instance of UserProfiler representing the user whose jolly flag needs to be reset.
    Returns:
        None
    """

    today = datetime.now()

    # Check if today is Monday and if it's past midnight
    if today.weekday() == 0 and today.hour == 0 and today.minute == 0:
        user.set_used_jolly(False)
        print("🤡 Jolly has been reset for the new week.")
