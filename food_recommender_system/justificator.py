import numpy as np
from dataloader import DataLoader
from datetime import datetime
from profiler import UserProfiler
import pandas as pd


class Justificator:
    """Provides explanations about fruits, vegetables, and meal choices based on nutritional data."""

    def __init__(self, df, seasonality):
        """Loads the nutritional database."""
        self.df = df
        self.seasonal_info = seasonality
        self.macronutrients = ["Calories", "Carbs", "Fats", "Fiber", "Protein"]

    def print_meal(meal: list, df: pd.DataFrame, servings: dict):    
        for food in meal:
            category = DataLoader.get_food_category(df, food)[0]
            serving_size = servings.get(category).get("serving_size")
            tips = servings.get(category).get("tips")
            print(f"- {serving_size}g of {food} ({tips})")

    def compare_meals(self, meal1: list, meal2: list, verbose: bool = False):

        if len(meal1) != len(meal2):
            return "Error: The two meals should have the same number of items for a fair comparison."

        comparison = ""
        comparison_results = []

        for food1, food2 in zip(meal1, meal2):
            food1_info = DataLoader.get_nutritional_info(self.df, food1, only_numbers=False)
            food2_info = DataLoader.get_nutritional_info(self.df, food2, only_numbers=False)

            if food1_info.size == 0 or food2_info.size == 0:
                return f"Error: Nutritional information for '{food1}' or '{food2}' is missing."

            if verbose:
                comparison = f"**Comparing {food1} vs {food2}:**\n"

            food1_info = np.array(food1_info[self.macronutrients])[0]
            food2_info = np.array(food2_info[self.macronutrients])[0]

            if verbose:
                comparison = f"\nComparing {food1} vs {food2}:\n"
            persuasion = "💡 Which one should you choose?\n"

            better_choice = {"food": None, "score": 0}  # Track which food is better based on nutrition

            for i, nutrient in enumerate(self.macronutrients):
                f1_value, f2_value = int(food1_info[i]), int(food2_info[i])

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
                persuasion += f"🔥 If you're trying to lose weight, {food1} is a lighter choice.\n"
            if food1_info[3] > food2_info[3]:  # More fiber is better for digestion
                persuasion += f"🌿 {food1} has more fiber, making it better for digestion and gut health.\n"
            if food1_info[4] > food2_info[4]:  # More protein helps with muscle growth
                persuasion += f"💪 If you're looking to build muscle, {food1} is the better option.\n"

            # Balanced advice
            persuasion += "😋 Remember that there is no good of bad food... Just follow your taste!\n"

            comparison_results.append(comparison + "\n" + persuasion)

        return comparison_results

    def recommend_seasonal(self, food_name):
        """
        Provides persuasive information about a fruit or vegetable, emphasizing its benefits and seasonality.

        Args:
            food_name (str): The name of the fruit or vegetable.

        Returns:
            str: Persuasive recommendation for choosing the food.
        """

        if food_name not in self.seasonal_info:
            return f"⚠️ Sorry, we don't have information on {food_name}."

        details = self.seasonal_info[food_name]

        recommendation = f"🌿 Why choose {food_name}?\n"
        # recommendation += f"📌 Description: {details['description']}\n"
        recommendation += f"💪 Health Benefits: {", ".join(details['benefits'])}\n"
        # recommendation += f"🛒 How to Choose: {details['how_to_choose']}\n"
        # recommendation += f"❄️ How to Store: {details['hot_to_store']}\n"
        recommendation += f"🥗 Nutritional Insights:\n{details['nutritional_intake']}\n"

        # Persuasive reasoning for seasonality
        recommendation += "\n🌍 Why choose seasonal produce?\n"
        recommendation += "✔️  Better taste & freshness – Seasonal foods are naturally ripened and have the best flavor.\n"
        recommendation += "✔️  Higher nutritional value – Fresh seasonal produce retains more vitamins and minerals.\n"
        recommendation += "✔️  Lower environmental impact – Locally grown seasonal food reduces transportation emissions.\n"

        # recommendation += "\n🍽️ Pro Tip: " + details["tips"] + "\n"

        return recommendation

    def get_current_meal(user: UserProfiler, df: pd.DataFrame):
        """Determines the current meal based on the time of day and provides recommendations."""
        today_day_of_week = datetime.now().weekday()
        current_hour = datetime.now().hour

        meal_name = "Breakfast" if current_hour < 9 else \
            "Snack" if current_hour < 11 else \
            "Lunch" if current_hour < 14 else \
            "Snack" if current_hour < 17 else "Dinner"

        current_meal = user.get_meals()[meal_name][today_day_of_week][0]
        current_alternative = user.get_meals()[meal_name][today_day_of_week][1]

        return meal_name, current_meal, current_alternative

        # print(f"Today's {meal} is:")
        # for food in current_meal:
        #     category = DataLoader.get_food_category(df, food)[0]
        #     print(f"- {food} ({category})")

        # print("\nAlternatively, you can have:")
        # for food in current_alternative:
        #     category = DataLoader.get_food_category(df, food)
        #     print(f"- {food} ({category[0] if category.size > 0 else 'Unknown'})")
