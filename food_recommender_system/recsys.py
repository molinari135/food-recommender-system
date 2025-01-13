import pandas as pd
import json
from profiler import UserProfileWithIntolerances
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class DataLoader:
    """A class to handle loading and preprocessing data for the recommender system."""

    def __init__(self, base_path="data/raw/"):
        self.base_path = base_path

    def load_csv(self, filename):
        """Load a CSV file and return a pandas DataFrame."""
        file_path = f"{self.base_path}{filename}"
        try:
            return pd.read_csv(file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file '{file_path}' not found.")

    def load_json(self, filename):
        """Load a JSON file and return its content as a Python dictionary."""
        file_path = f"{self.base_path}{filename}"
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file '{file_path}' not found.")

    @staticmethod
    def filter_categories(df, exclude_categories):
        """Filter out rows with specific category names."""
        return df[~df['Category Name'].isin(exclude_categories)]

    @staticmethod
    def fill_missing_values(df, fill_value=0):
        """Replace NaN values with a specified fill value."""
        return df.fillna(fill_value)

    @staticmethod
    def validate_seasonal_foods(nutritional_df, seasonality_data, country='Italy'):
        """
        Validate that all seasonal food names from the JSON file
        are present in the nutritional DataFrame.
        """
        # Extract seasonal food names for the given country
        seasonal_food_names = []
        for month, foods in seasonality_data[country].items():
            seasonal_food_names.extend(foods)

        # Convert to lowercase for consistency
        seasonal_food_names = [food.lower() for food in seasonal_food_names]
        nutritional_df['Food Name'] = nutritional_df['Food Name'].str.lower()

        # Check for missing food names
        missing_food_names = [food for food in seasonal_food_names if food not in nutritional_df['Food Name'].values]

        if not missing_food_names:
            print("All seasonal food names are present in the dataset.")
        else:
            print("The following seasonal food names are missing in the dataset:")
            print(missing_food_names)


class RecommenderSystem:
    def __init__(self, nutritional_df, food_pantry, seasonality_data):
        self.nutritional_df = nutritional_df
        self.food_pantry = food_pantry
        self.seasonality_data = seasonality_data

    def find_similar_ingredients(self, base_ingredients, top_n=3):
        """
        Finds similar ingredients to those in the user profile based on nutritional data.

        base_ingredients: List of ingredients from the user's pantry.
        top_n: The number of similar ingredients to return for each base ingredient.

        Returns: A dictionary of similar ingredients for each base ingredient.
        """
        # Ensure there are no NaN values
        if self.nutritional_df.isnull().values.any():
            print("Missing values detected, filling NaN values with 0...")
            self.nutritional_df = self.nutritional_df.fillna(0)

        # Drop non-nutritional columns
        nutrition_matrix = self.nutritional_df.drop(columns=['Food Name', 'Category Name']).values

        # Compute the cosine similarity matrix
        similarity_matrix = cosine_similarity(nutrition_matrix)

        # Initialize dictionary for similar ingredients
        similar_ingredients = {}

        for ingredient in base_ingredients:
            ingredient = ingredient.strip().lower()
            matching_rows = self.nutritional_df[self.nutritional_df['Food Name'] == ingredient]

            if matching_rows.empty:
                print(f"Ingredient '{ingredient}' not found in the dataset!")
                similar_ingredients[ingredient] = []
                continue

            # Get the index and category of the base ingredient
            index = matching_rows.index[0]
            ingredient_category = matching_rows['Category Name'].iloc[0]

            # Filter the nutritional data by the same category
            category_filtered_df = self.nutritional_df[self.nutritional_df['Category Name'] == ingredient_category]

            # Recompute the cosine similarity matrix for the filtered category data
            category_nutrition_matrix = category_filtered_df.drop(columns=['Food Name', 'Category Name']).values
            category_similarity_matrix = cosine_similarity(category_nutrition_matrix)

            # Get the similarities for the current ingredient in the filtered matrix
            ingredient_similarities = category_similarity_matrix[category_filtered_df.index == index].flatten()

            # Get the indices of the most similar ingredients (excluding the ingredient itself)
            similar_indices = np.argsort(ingredient_similarities)[::-1][1:top_n + 1]

            # Get the food names for the similar ingredients
            similar_foods = [category_filtered_df.iloc[i]['Food Name'] for i in similar_indices]

            # Add the result to the dictionary
            similar_ingredients[ingredient] = similar_foods

        return similar_ingredients


if __name__ == "__main__":
    # Initialize DataLoader
    data_loader = DataLoader()

    # Load files
    nutritional_facts = data_loader.load_csv("nutritional-facts.csv")
    food_seasonality = data_loader.load_json("food-seasonality.json")
    food_pantry = data_loader.load_json("food-pantry.json")

    # Filter categories
    exclude_categories = ['Baby Foods', 'Meals, Entrees, and Side Dishes', 'Fast Foods']
    nutritional_facts = DataLoader.filter_categories(nutritional_facts, exclude_categories)
    nutritional_facts = DataLoader.fill_missing_values(nutritional_facts)

    print(nutritional_facts.head())
    DataLoader.validate_seasonal_foods(nutritional_facts, food_seasonality, country='Italy')

    profiler = UserProfileWithIntolerances()
    user_profile = profiler.create_user_profile()

    if user_profile:
        # Apply dietary filters from the user profile
        filtered_foods = profiler.filter_food_based_on_user_profile(user_profile, nutritional_facts)

        # Initialize RecommenderSystem with the necessary data
        recommender = RecommenderSystem(nutritional_df=filtered_foods,
                                        food_pantry=food_pantry,
                                        seasonality_data=food_seasonality)

        # Get similar ingredients based on the user's available ingredients
        base_ingredients = user_profile["available_ingredients"]['Base']

        similar_ingredients = recommender.find_similar_ingredients(base_ingredients)

        # Print the similar ingredients for each base ingredient
        for ingredient, similar in similar_ingredients.items():
            print(f"Base Ingredient: {ingredient}")
            print(f"Similar Ingredients: {', '.join(similar)}\n")
