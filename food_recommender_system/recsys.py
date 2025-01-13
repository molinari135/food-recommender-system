import pandas as pd
import json
from profiler import UserProfileWithIntolerances


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
        filtered_foods = profiler.filter_food_based_on_user_profile(user_profile, nutritional_facts)