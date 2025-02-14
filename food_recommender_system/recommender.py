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
        """
        Get the seasonal fruits and vegetables for a given nationality.
        Args:
            nationality (str): The nationality to get the seasonal food for. Defaults to "Italy".
        Returns:
            tuple: A tuple containing two lists:
                - fruits (list): A list of seasonal fruits.
                - vegetables (list): A list of seasonal vegetables.
        """

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
        """
        Get a list of foods similar to the given food based on nutritional information.
        Parameters:
        df (pd.DataFrame): DataFrame containing nutritional information of various foods.
        food_name (str): The name of the food to find similar foods for.
        same_category (bool, optional): If True, only consider foods in the same category as the given food. Default is True.
        low_density_food (bool, optional): If True, sort similar foods by energy density. Default is True.
        Returns:
        list: A list of tuples containing similar foods and their similarity scores. If low_density_food is True,
              each tuple also includes the energy density of the food.
        """

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
        """
        Asks the user for their food preferences based on categories and intolerances,
        and saves the preferences to a profile.
        Parameters:
        filename (Path): The path where the user profile will be saved.
        The function performs the following steps:
        1. Sets default preferences based on user intolerances.
        2. Filters the dataframe to exclude certain categories and intolerances.
        3. Prompts the user to select their preferred foods from each category.
        4. Combines the selected preferences into a single dataframe.
        5. Saves the user's food preferences to a profile.
        If no preferences are selected for a category, default preferences are used.
        If the combined preferences dataframe is empty, the original filtered data is used.
        """

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
        """
        Prompts the user to select their preferred seasonal fruits and vegetables for the current month,
        and saves these preferences to a user profile.
        Args:
            filename (Path): The path to the file where the user profile will be saved.
            info_file (dict): A dictionary containing information about various foods, including their benefits,
                              how to choose them, how to store them, and additional tips.
        Returns:
            None
        """

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
