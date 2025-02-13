import pandas as pd
import numpy as np
from numpy.linalg import norm
from datetime import datetime
from pathlib import Path

from dataloader import DataLoader
from profiler import UserProfiler
from config import EXCLUDED_CATEGORIES, PREFERENCES, LACTOSE_INTOLERANCE, GLUTEN_INTOLERANCE, LACTOSE_AND_GLUTEN_INTOLERANCE


class RecommenderSystem:
    def __init__(self, df: pd.DataFrame, seasonality: dict, user_profiler: UserProfiler):
        self.df = df
        self.seasonality = seasonality
        self.user_profiler = user_profiler

    def get_seasonal_food(self, nationality: str = "Italy"):
        fruits = []
        vegetables = []

        current_month = datetime.now().strftime("%m")
        seasonal_food = self.seasonality.get(nationality, {}).get(current_month, [])

        for food in seasonal_food:
            food_category = self.df[self.df["Food Name"] == food]["Category Name"].values

            if len(food_category) > 0:
                category = food_category[0]

                if category == "Fruits":
                    fruits.append(food)
                elif category == "Vegetables":
                    vegetables.append(food)

        return fruits, vegetables

    @staticmethod
    def get_similar_food(df: pd.DataFrame, food_name: str, same_category: bool = True, low_density_food: bool = True):
        similar_foods = []

        if same_category:
            food_info = DataLoader.get_nutritional_info(df, food_name, only_numbers=False)
            if food_info is None:
                return f"No information found for {food_name}"

            category = food_info["Category Name"].values[0]
            food_A = DataLoader.get_nutritional_info(df, food_name).to_numpy().flatten()

            for food in df[df["Category Name"] == category]["Food Name"]:
                if food == food_name:
                    continue
                food_B = DataLoader.get_nutritional_info(df, food).to_numpy().flatten()

                norm_A = norm(food_A)
                norm_B = norm(food_B)

                if norm_A == 0 or norm_B == 0:
                    similarity = 0
                else:
                    similarity = np.dot(food_A, food_B) / (norm_A * norm_B)

                similar_foods.append((food, similarity))

            similar_foods = sorted(similar_foods, key=lambda x: x[1], reverse=True)

            if low_density_food:
                similar_foods = sorted(similar_foods, key=lambda x: (DataLoader.compute_energy_density(df, x[0])[1], x[1]))
                similar_foods = [(food, similarity, DataLoader.compute_energy_density(df, food)[0]) for food, similarity in similar_foods]

            return similar_foods

    def ask_user_preferences(self, filename: Path):
        preferences = {}
        # Set the default preferences
        default_preferences = PREFERENCES["no_intolerances"]

        # Remove those categories that are not required
        filtered_df = DataLoader.filter_categories(self.df, EXCLUDED_CATEGORIES)
        # Get all category names from the filtered dataframe
        categories = filtered_df["Category Name"].unique()
        # Get user intolerances to update default preferences
        user_intolerances = self.user_profiler.get_intolerances()

        if user_intolerances == LACTOSE_INTOLERANCE:
            print("Loading default preferences for dairy intolerances...")
            default_preferences = PREFERENCES["lactose_intolerance"]
        if user_intolerances == GLUTEN_INTOLERANCE:
            print("Loading default preferences for gluten intolerances...")
            default_preferences = PREFERENCES["gluten_intolerance"]
        if user_intolerances == LACTOSE_AND_GLUTEN_INTOLERANCE:
            print("Loading default preferences for dairy and gluten intolerances...")
            default_preferences = PREFERENCES["lactose_and_gluten_intolerance"]

        # Filter again the dataframe taking into account intolerances
        data = DataLoader.filter_categories(filtered_df, user_intolerances)
        if user_intolerances != []:
            # Remove those categories related to intolerances
            categories = np.setdiff1d(categories, user_intolerances)

        print("In order to create your profile, follow the instructions below.")

        for category in categories:
            foods = data[data["Category Name"] == category]["Food Name"].tolist()

            print(f"\n{category}:")
            for i, food in enumerate(foods, 1):
                print(f"{i}. {food}")

            while True:
                try:
                    choices = input(f"Select {category} (1-{len(foods)}): ")
                    if not choices:
                        print(f"Nothing has been chosen for {category}, loading default preferences...")
                        preferences[category] = default_preferences[category]
                        break

                    selected = [int(x) for x in choices.split()]

                    if all(1 <= x <= len(foods) for x in selected):
                        preferences[category] = [foods[i - 1] for i in selected]
                        break
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter valid numbers separated by spaces.")

        # Combine all preferences into a single dataframe
        combined_preferences = pd.concat(
            [data[data["Food Name"].isin(preferences[category])] for category in preferences]
        )

        # If combined_preferences is empty, fallback to data
        if combined_preferences.empty:
            return data

        food_list = combined_preferences["Food Name"].unique()
        self.user_profiler.set_food_preferences(food_list.tolist())
        self.user_profiler.save_profile(filename)

        print("\n✅ Preferences saved successfully!")

    def ask_seasonal_preferences(self, filename: Path, info_file: dict):

        food_info = info_file
        # Get seasonal fruits and vegetables
        fruits, vegetables = self.get_seasonal_food()

        print("Please select your preferred seasonal fruits and vegetables for this month.")
        print("Enter numbers separated by spaces, or press Enter to select all.")

        # Function to display food with benefits
        def display_food_options(food_list, food_type):
            print(f"\nSeasonal {food_type}:")
            for i, food in enumerate(food_list, 1):
                benefits = ", ".join(food_info.get(food, {}).get("benefits", ["No data available"]))
                print(f"{i}. {food} (Benefits: {benefits})")
            return food_list

        # Get user preferences for seasonal fruits
        fruits_list = display_food_options(fruits, "Fruits")
        selected_fruits = input(f"Select fruits (1-{len(fruits)}): ").strip()
        if selected_fruits:
            selected_fruits = [fruits_list[int(i) - 1] for i in selected_fruits.split()]
        else:
            selected_fruits = fruits

        # Get user preferences for seasonal vegetables
        vegetables_list = display_food_options(vegetables, "Vegetables")
        selected_vegetables = input(f"Select vegetables (1-{len(vegetables)}): ").strip()
        if selected_vegetables:
            selected_vegetables = [vegetables_list[int(i) - 1] for i in selected_vegetables.split()]
        else:
            selected_vegetables = vegetables

        # Show additional information after selection
        print("\nHere are some tips for your selected foods:")
        for food in selected_fruits + selected_vegetables:
            how_to_choose = food_info.get(food, {}).get("how_to_choose", "No information available")
            how_to_store = food_info.get(food, {}).get("how_to_store", "No information available")
            tips = food_info.get(food, {}).get("tips", "No tips available")

            print(f"\n📌 {food.upper()}")
            print(f"🛒 How to Choose: {how_to_choose}")
            print(f"❄️ How to Store: {how_to_store}")
            print(f"💡 Tips: {tips}")

        # Filter the user preferences dataframe to include only selected seasonal fruits and vegetables
        selected_fruits_df = self.df[self.df['Food Name'].isin(selected_fruits)]
        selected_vegetables_df = self.df[self.df['Food Name'].isin(selected_vegetables)]

        # Add selected preferences to combined_preferences
        combined_preferences = pd.concat([selected_fruits_df, selected_vegetables_df])

        # Save selected seasonal preferences
        food_list = combined_preferences["Food Name"].unique()
        self.user_profiler.set_seasonal_preferences(food_list.tolist())
        self.user_profiler.save_profile(filename)

        print("\n✅ Seasonal preferences saved successfully!")
        