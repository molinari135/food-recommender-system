import numpy as np
from dataloader import DataLoader
from datetime import datetime
from profiler import UserProfiler
import pandas as pd
from pathlib import Path

import time


class Justificator:
    """Provides explanations about fruits, vegetables, and meal choices based on nutritional data."""

    def __init__(self, df, seasonality):
        """Loads the nutritional database."""

        self.df = df
        self.seasonal_info = seasonality
        self.macronutrients = ["Calories", "Carbs", "Fats", "Fiber", "Protein"]

    @staticmethod
    def print_meal(meal: list, df: pd.DataFrame, servings: dict):
        """
        Prints the meal details including serving size and tips for each food item.

        Args:
            meal (list): A list of food items to be printed.
            df (pd.DataFrame): A DataFrame containing food data.
            servings (dict): A dictionary containing serving size and tips for each food category.

        Returns:
            None
        """

        for food in meal:
            category = DataLoader.get_food_category(df, food)[0]
            serving_size = servings.get(category).get("serving_size")
            tips = servings.get(category).get("tips")
            print(f"- {serving_size}g of {food} ({tips})")

    @staticmethod
    def print_full_week_meals(user: UserProfiler, df: pd.DataFrame, servings: dict):
        """
        Prints the full week's meal plan for the user.
        Args:
            user (UserProfiler): An instance of UserProfiler containing user-specific meal data.
            df (pd.DataFrame): A DataFrame containing meal information.
            servings (dict): A dictionary containing serving sizes for each meal.
        Returns:
            None
        """

        meal_types = ["Breakfast", "Snack", "Lunch", "Snack", "Dinner"]
        week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        meals = user.get_meals()

        for day_idx, day in enumerate(week_days):
            print(f"\n📅 {day}:")

            for meal in meal_types:
                if meal in meals:
                    if day_idx < len(meals[meal]):
                        meal_data = meals[meal][day_idx]
                        main_meal, alternative_meal = meal_data[:2]

                        print(f"\n🍽️  {meal}:")
                        print("👉 Main option:")
                        Justificator.print_meal(main_meal, df, servings)

                        print("\n🔄 Alternative option:")
                        Justificator.print_meal(alternative_meal, df, servings)

                        if len(meal_data) == 3:
                            chosen_meal = meal_data[2]
                            print("\n✅ Chosen option:")
                            Justificator.print_meal(chosen_meal, df, servings)

                        print("-" * 30)
            time.sleep(0.5)

    def compare_meals(self, meal1: list, meal2: list, verbose: bool = False):
        """
        Compare two meals based on their nutritional information.
        Args:
            meal1 (list): A list of food items representing the first meal.
            meal2 (list): A list of food items representing the second meal.
            verbose (bool, optional): If True, provides detailed comparison information. Defaults to False.
        Returns:
            list: A list of strings containing the comparison results and recommendations.
                  If there is an error (e.g., missing nutritional information), returns an error message.
        """

        if len(meal1) != len(meal2):
            return "🔴 Error: The two meals should have the same number of items for a fair comparison."

        comparison = ""
        comparison_results = []

        for food1, food2 in zip(meal1, meal2):
            food1_info = DataLoader.get_nutritional_info(self.df, food1, only_numbers=False)
            food2_info = DataLoader.get_nutritional_info(self.df, food2, only_numbers=False)

            if food1_info.size == 0 or food2_info.size == 0:
                return f"🔴 Error: Nutritional information for '{food1}' or '{food2}' is missing."

            if verbose:
                comparison = f"**Comparing {food1} vs {food2}:**\n"

            food1_info = np.array(food1_info[self.macronutrients])[0]
            food2_info = np.array(food2_info[self.macronutrients])[0]

            if verbose:
                comparison = f"\nComparing {food1} vs {food2}:\n"
            # persuasion = "💡 Which one should you choose?\n"
            persuasion = ""

            better_choice = {"food": None, "score": 0}  # Track which food is better based on nutrition

            for i, nutrient in enumerate(self.macronutrients):
                f1_value = int(food1_info[i]) if pd.notna(food1_info[i]) else 0
                f2_value = int(food2_info[i]) if pd.notna(food2_info[i]) else 0

                if f1_value < f2_value:
                    if verbose:
                        comparison += f"- {nutrient}: {food1} has less ({f1_value}), {food2} has more ({f2_value}).\n"
                    if nutrient in ["Calories", "Carbs", "Fats"]:
                        better_choice["food"] = food1  # Lower calories/carbs/fats = usually healthier
                        better_choice["score"] += 1
                elif f1_value > f2_value:
                    if verbose:
                        comparison += f"- {nutrient}: {food1} has more ({f1_value}), {food2} has less ({f2_value}).\n"
                    if nutrient in ["Protein", "Fiber"]:
                        better_choice["food"] = food1  # More protein/fiber = usually healthier
                        better_choice["score"] += 1
                elif f1_value == f2_value:
                    if verbose:
                        comparison += f"- {nutrient}: Both have the same amount ({f1_value}).\n"

            # Persuasion logic
            if better_choice["food"]:
                if better_choice["food"] == food1:
                    persuasion += f"👉 {food1} has better macronutrient balance.\n"
                else:
                    persuasion += f"👉 {food2} is a better option if you're looking for a healthier alternative.\n"

            # Additional tailored reasoning
            if food1_info[0] < food2_info[0]:  # Lower calories is generally healthier
                persuasion += f"🔥 If you're trying to lose weight, {food1} is a lighter choice."
            if food1_info[3] > food2_info[3]:  # More fiber is better for digestion
                persuasion += f"🌿 {food1} has more fiber, making it better for digestion and gut health."
            if food1_info[4] > food2_info[4]:  # More protein helps with muscle growth
                persuasion += f"💪 If you're looking to build muscle, {food1} is the better option because it has more proteins."

            comparison_results.append(comparison + persuasion)
        comparison_results.append("😋 Remember that there is no good of bad food... Just follow your taste!\n")

        return comparison_results

    def recommend_seasonal(self, food_name: str) -> str:
        """
        Recommend seasonal information for a given food item.
        Args:
            food_name (str): The name of the food item to get recommendations for.
        Returns:
            str: A string containing the recommendation, including health benefits,
                 nutritional insights, and reasons for choosing seasonal produce.
                 If the food item is not found, a warning message is returned.
        """

        if food_name not in self.seasonal_info:
            return f"⚠️ Sorry, we don't have information on {food_name}."

        details = self.seasonal_info[food_name]

        recommendation = f"🌿 Why choose {food_name}?\n"
        recommendation += f"💪 Health Benefits: {", ".join(details['benefits'])}\n"
        recommendation += f"🥗 Nutritional Insights:\n{details['nutritional_intake']}\n"

        # Persuasive reasoning for seasonality
        recommendation += "\n🌍 Why choose seasonal produce?\n"
        recommendation += "✔️  Better taste & freshness – Seasonal foods are naturally ripened and have the best flavor.\n"
        recommendation += "✔️  Higher nutritional value – Fresh seasonal produce retains more vitamins and minerals.\n"
        recommendation += "✔️  Lower environmental impact – Locally grown seasonal food reduces transportation emissions.\n"

        return recommendation

    def get_current_meal(user: UserProfiler, meal_name: str = None, debug: bool = False):
        """
        Determines the current meal based on the time of day and provides recommendations.
        Args:
            user (UserProfiler): An instance of UserProfiler containing user meal preferences.
            meal_name (str, optional): The name of the meal to retrieve. If None, the meal is determined based on the current time. Defaults to None.
            debug (bool, optional): If True, uses the provided meal_name regardless of the current time. Defaults to False.
        Returns:
            tuple: A tuple containing:
                - meal_name (str): The name of the determined meal.
                - current_meal (str): The primary meal recommendation.
                - current_alternative (str): An alternative meal recommendation.
                - choosen_meal (str or None): The user's preferred meal if specified, otherwise None.
        """

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
            # TODO This is the real expression of the user preferences!
            choosen_meal = user.get_meals()[meal_name][today_day_of_week][2]
        else:
            choosen_meal = None

        return meal_name, current_meal, current_alternative, choosen_meal

    def choose_foods_in_current_meal(user: UserProfiler, filename: Path):
        """
        Asks the user to choose between individual foods in the main meal and the alternative meal for the current meal.
        Parameters:
        user (UserProfiler): The user profile object containing meal information.
        filename (Path): The path to the file where the user profile is saved.
        Returns:
        None
        """

        meal_name, current_meal, current_alternative, choosen_meal = Justificator.get_current_meal(user, meal_name="Lunch", debug=True)

        # Check if the meal already has a chosen meal
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
