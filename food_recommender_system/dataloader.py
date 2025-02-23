import json
import pandas as pd
from pathlib import Path
from typing import Tuple
from food_recommender_system.config import RAW_DATA_PATH


class DataLoader:
    """A class to handle loading and preprocessing data for the recommender system."""

    def __init__(self, base_path: Path = RAW_DATA_PATH):
        self.base_path = base_path

    def load_csv(self, filename: Path):
        """Load a CSV file and return a pandas DataFrame."""
        try:
            return pd.read_csv(self.base_path / filename)
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file '{filename}' not found.")

    def load_json(self, filename: Path):
        """Load a JSON file and return its content as a Python dictionary."""
        try:
            with open(self.base_path / filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file '{filename}' not found.")

    @staticmethod
    def filter_categories(df: pd.DataFrame, exclude_categories: list) -> pd.DataFrame:
        """Filter out rows with specific category names."""
        return df[~df['Category Name'].isin(exclude_categories)]

    @staticmethod
    def fill_missing_values(df: pd.DataFrame, fill_value: int = 0):
        """Replace NaN values with a specified fill value."""
        return df.fillna(fill_value, inplace=True)

    @staticmethod
    def get_nutritional_info(df: pd.DataFrame, food_name: str, only_numbers: bool = True) -> pd.DataFrame:
        """
        Retrieve nutritional information for a specific food item from a DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing nutritional information.
            food_name (str): The name of the food item to retrieve information for.
            only_numbers (bool, optional): If True, return only numerical columns (excluding "Food Name" and "Category Name"). Defaults to True.

        Returns:
            pd.DataFrame: A DataFrame containing the nutritional information for the specified food item.
                          Returns None if the food item is not found.
        """
        food_info = df[df["Food Name"] == food_name]
        if len(food_info) > 0:
            if only_numbers:
                return food_info.drop(columns=["Food Name", "Category Name"])
            return food_info
        return None

    @staticmethod
    def compute_energy_density(df: pd.DataFrame, food_name: str) -> Tuple[str, float]:
        """
        Computes the energy density of a given food item based on its nutritional information.
        Parameters:
        df (pd.DataFrame): DataFrame containing nutritional information of various food items.
        food_name (str): The name of the food item for which to compute the energy density.
        Returns:
        Tuple[str, float]: A tuple containing a string indicating the energy density category
                           ("Low", "Medium", "High") and the energy density value.
                           If the food item is not found, returns a string with an error message.
        """
        food_info = DataLoader.get_nutritional_info(df, food_name)
        if isinstance(food_info, str):
            return food_info
        energy_density = food_info["Calories"].values[0] / 100

        if energy_density < 1.5:
            return ("Low", energy_density)
        if 1.5 <= energy_density <= 2.5:
            return ("Medium", energy_density)
        return ("High", energy_density)

    @staticmethod
    def get_food_category(df: pd.DataFrame, food_name: str) -> str:
        return df[df["Food Name"] == food_name]["Category Name"].values
