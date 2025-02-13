from datetime import datetime
from profiler import UserProfiler
from justificator import Justificator
from pathlib import Path
import pandas as pd
import random


def change_meal(user: UserProfiler, df: pd.DataFrame, fast_food_equiv: dict, meal_name: str, servings: dict, filename: Path):
    """Suggest a new meal based on user mood and preferences."""

    today_day_of_week = datetime.now().weekday()
    weekly_meals = user.get_meals()

    has_used_jolly = user.get_used_jolly()

    if has_used_jolly:
        print(f"Have a nice {meal_name.lower()}!")
    else:
        if meal_name == "Lunch" or meal_name == "Dinner":
            is_stressed = input("Are you feeling stressed today? (yes/no): ").strip().lower() == 'yes'

            if is_stressed:
                print(f"🤔 Let's see, today's {meal_name.lower()} is...")
                Justificator.get_current_meal(user, df)
                print("😉 Just for today, let's eat something that could improve your mood!")

                fast_foods = df[df["Category Name"] == "Fast Foods"]

                fast_food = random.choice(fast_foods["Food Name"].to_list())
                new_lunch = [[fast_food]]
                food_equivalents = fast_food_equiv.get(fast_food)

                if food_equivalents:
                    new_lunch.append(food_equivalents)

                weekly_meals[meal_name][today_day_of_week] = new_lunch

                user.set_used_jolly(True)
                print(f"\nToday you can have: a {", ".join(weekly_meals[meal_name][today_day_of_week][0])}")
                # Justificator.print_meal(weekly_meals[meal_name][today_day_of_week][0], df, servings)
                print(f"Alternatively, you can make a {", ".join(weekly_meals[meal_name][today_day_of_week][1])}")

                user.set_meals(weekly_meals)
                user.save_profile(filename)
                print("\n🫡 Take care of yourself!")
        else:
            print(f"Have a nice {meal_name.lower()}!")


def reset_jolly_if_new_week(user: UserProfiler):
    """Reset the jolly flag if today is the first day of the week (Monday)."""
    today = datetime.now()

    # Check if today is Monday and if it's past midnight
    if today.weekday() == 0 and today.hour == 0 and today.minute == 0:
        user.set_used_jolly(False)
        print("Jolly has been reset for the new week.")
