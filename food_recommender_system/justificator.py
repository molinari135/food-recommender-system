import numpy as np
from food_recommender_system.dataloader import DataLoader
from datetime import datetime
from food_recommender_system.profiler import UserProfiler
import pandas as pd
from pathlib import Path
import time

from config import MACRONUTRIENTS


def print_meal(meal: list, df: pd.DataFrame, servings: dict):
    for food in meal:
        category = DataLoader.get_food_category(df, food)[0]
        serving_size = servings.get(category).get("serving_size")
        tips = servings.get(category).get("tips")
        print(f"- {serving_size}g of {food} ({tips})")


def print_full_week_meals(user: UserProfiler, df: pd.DataFrame, servings: dict):
    meal_types = ["Breakfast", "Snack", "Lunch", "Snack", "Dinner"]
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    meals = user.get_meals()
    csv_data = []

    output_choice = input("Do you want to print the meals in the terminal or save them to a CSV file? (print/csv): ").strip().lower()

    for day_idx, day in enumerate(week_days):
        if output_choice == "print":
            print(f"\n📅 {day}:")

        for meal in meal_types:
            if meal in meals:
                if day_idx < len(meals[meal]):
                    meal_data = meals[meal][day_idx]
                    main_meal, alternative_meal = meal_data[:2]

                    if output_choice == "print":
                        print(f"\n🍽️  {meal}:")
                        print("👉 Main option:")
                        print_meal(main_meal, df, servings)
                        print("\n🔄 Alternative option:")
                        print_meal(alternative_meal, df, servings)
                        if len(meal_data) == 3:
                            chosen_meal = meal_data[2]
                            print("\n✅ Chosen option:")
                            print_meal(chosen_meal, df, servings)
                        print("-" * 30)
                    elif output_choice == "csv":
                        csv_data.append([day, meal, "Main", ', '.join(main_meal)])
                        csv_data.append([day, meal, "Alternative", ', '.join(alternative_meal)])
                        if len(meal_data) == 3:
                            chosen_meal = meal_data[2]
                            csv_data.append([day, meal, "Chosen", ', '.join(chosen_meal)])

        if output_choice == "print":
            time.sleep(0.5)

    if output_choice == "csv":
        # Save to CSV
        csv_df = pd.DataFrame(csv_data, columns=["Day", "Meal Type", "Option Type", "Foods"])
        pivot_df = csv_df.pivot_table(index=["Meal Type", "Option Type"], columns="Day", values="Foods", aggfunc=lambda x: ' | '.join(x))
        pivot_df.to_csv("weekly_meals.csv")
        print("\n📁 Weekly meals have been saved to 'weekly_meals.csv'.")


def compare_meals(df: pd.DataFrame, meal1: list, meal2: list, verbose: bool = False):
    if len(meal1) != len(meal2):
        return "🔴 Error: The two meals should have the same number of items for a fair comparison."

    comparison_results = []

    for food1, food2 in zip(meal1, meal2):
        food1_info = DataLoader.get_nutritional_info(df, food1, only_numbers=False)
        food2_info = DataLoader.get_nutritional_info(df, food2, only_numbers=False)

        if food1_info.size == 0 or food2_info.size == 0:
            return f"🔴 Error: Nutritional information for '{food1}' or '{food2}' is missing."

        if verbose:
            comparison = f"**Comparing {food1} vs {food2}:**\n"
        else:
            comparison = ""

        food1_info = np.array(food1_info[MACRONUTRIENTS])[0]
        food2_info = np.array(food2_info[MACRONUTRIENTS])[0]

        if verbose:
            comparison = f"\nComparing {food1} vs {food2}:\n"
        persuasion = ""

        better_choice = {"food": None, "score": 0}

        for i, nutrient in enumerate(MACRONUTRIENTS):
            f1_value = int(food1_info[i]) if pd.notna(food1_info[i]) else 0
            f2_value = int(food2_info[i]) if pd.notna(food2_info[i]) else 0

            if f1_value < f2_value:
                if verbose:
                    comparison += f"- {nutrient}: {food1} has less ({f1_value}), {food2} has more ({f2_value}).\n"
                if nutrient in ["Calories", "Carbs", "Fats"]:
                    better_choice["food"] = food2
                    better_choice["score"] += 1
                else:
                    better_choice["food"] = food1
                    better_choice["score"] += 1
            elif f1_value > f2_value:
                if verbose:
                    comparison += f"- {nutrient}: {food1} has more ({f1_value}), {food2} has less ({f2_value}).\n"
                if nutrient in ["Protein", "Fiber"]:
                    better_choice["food"] = food2
                    better_choice["score"] += 1
                else:
                    better_choice["food"] = food1
                    better_choice["score"] += 1
            elif f1_value == f2_value:
                if verbose:
                    comparison += f"- {nutrient}: Both have the same amount ({f1_value}).\n"

        if better_choice["food"]:
            if better_choice["food"] == food2:
                persuasion += f"\n👉 {food2} has better macronutrient balance."
            else:
                persuasion += f"\n👉 {food1} is also a good option if you're looking for an alternative."

        if food2_info[0] < food1_info[0]:
            persuasion += f"\n🔥 If you're trying to lose weight, {food2} is a lighter choice."
        if food2_info[3] > food1_info[3]:
            persuasion += f"\n🌿 {food2} has more fiber, making it better for digestion and gut health."
        if food2_info[4] > food1_info[4]:
            persuasion += f"\n💪 If you're looking to build muscle, {food2} is the better option because it has more proteins."

        comparison_results.append(comparison + persuasion)
    comparison_results.append("\n😋 Remember that there is no good or bad food... Just follow your taste!\n")

    return comparison_results


def recommend_seasonal(seasonal_info: dict, food_name: str) -> str:
    if food_name not in seasonal_info:
        return f"⚠️ Sorry, we don't have information on {food_name}."

    details = seasonal_info[food_name]

    recommendation = f"🌿 Why choose {food_name}?\n"
    recommendation += f"💪 Health Benefits: {', '.join(details['benefits'])}\n"
    recommendation += f"🥗 Nutritional Insights:\n{details['nutritional_intake']}\n"

    recommendation += "\n🌍 Why choose seasonal produce?\n"
    recommendation += "✔️  Better taste & freshness – Seasonal foods are naturally ripened and have the best flavor.\n"
    recommendation += "✔️  Higher nutritional value – Fresh seasonal produce retains more vitamins and minerals.\n"
    recommendation += "✔️  Lower environmental impact – Locally grown seasonal food reduces transportation emissions.\n"

    return recommendation


def get_current_meal(user: UserProfiler, meal_name: str = None, debug: bool = False):
    today_day_of_week = datetime.now().weekday()
    current_hour = datetime.now().hour

    if debug:
        meal_name = meal_name
    else:
        meal_name = "Breakfast" if current_hour < 9 else \
            "Snack" if current_hour < 11 else \
            "Lunch" if current_hour < 14 else \
            "Snack" if current_hour < 17 else "Dinner"

    current_meal = user.get_meals()[meal_name][today_day_of_week][0]
    current_alternative = user.get_meals()[meal_name][today_day_of_week][1]

    if len(user.get_meals()[meal_name][today_day_of_week]) == 3:
        choosen_meal = user.get_meals()[meal_name][today_day_of_week][2]
    else:
        choosen_meal = None

    return meal_name, current_meal, current_alternative, choosen_meal


def choose_foods_in_current_meal(user: UserProfiler, filename: Path, df: pd.DataFrame):
    meal_name, current_meal, current_alternative, choosen_meal = get_current_meal(user)

    if choosen_meal:
        return

    print(f"\n🍽️ {meal_name}:")
    chosen_meal = []
    for i, (main_food, alt_food) in enumerate(zip(current_meal, current_alternative)):
        if main_food == alt_food:
            chosen_meal.append(main_food)
            continue

        print(f"\n👉 Option 1: {main_food}")
        print(f"🔄 Option 2: {alt_food}")

        # Print comparison between the foods
        comparison = compare_meals(df, [main_food], [alt_food], verbose=True)
        for line in comparison:
            print(line)

        choice = input(f"Which option do you prefer for item {i + 1}? (1/2): ").strip()
        if choice == "1":
            chosen_meal.append(main_food)
        elif choice == "2":
            chosen_meal.append(alt_food)
        else:
            print("⚠️ Invalid choice. Keeping the main option.")
            chosen_meal.append(main_food)

    meals = user.get_meals()
    today_day_of_week = datetime.now().weekday()
    meals[meal_name][today_day_of_week] = [current_meal, current_alternative, chosen_meal]
    user.set_meals(meals)
    user.save_profile(filename)
    print("-" * 30)
