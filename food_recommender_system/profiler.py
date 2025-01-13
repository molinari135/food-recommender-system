import json
import pandas as pd

class UserProfiler:
    """
    A class to create and manage user profiles for the recommender system.
    """
    
    def __init__(self, pantry_path="data/raw/food-pantry.json"):
        """
        Initialize the profiler with the path to the pantry data.
        :param pantry_path: Path to the JSON file containing pantry data.
        """
        self.pantry_path = pantry_path

    def get_pantry(self, nationality):
        """
        Retrieve the pantry for the specified nationality.
        :param nationality: User's nationality as a string.
        :return: A dictionary of pantry ingredients categorized by type, or None if not found.
        """
        try:
            with open(self.pantry_path, 'r') as file:
                pantries = json.load(file)
            return pantries.get(nationality, None)
        except FileNotFoundError:
            raise FileNotFoundError(f"Pantry file '{self.pantry_path}' not found.")

    @staticmethod
    def ask_about_ingredients(ingredients):
        """
        Ask the user which ingredients they have.
        :param ingredients: List of ingredient names.
        :return: List of ingredients the user has available.
        """
        available_ingredients = []
        for ingredient in ingredients:
            response = input(f"Do you have {ingredient}? (yes/no): ").strip().lower()
            if response == 'yes':
                available_ingredients.append(ingredient)
        return available_ingredients

    def create_user_profile(self):
        """
        Create a user profile based on their nationality and available ingredients, 
        as well as intolerances and allergies.
        :return: A dictionary containing the user's nationality, available ingredients, 
                and dietary preferences (intolerances/allergies).
        """
        # Ask for intolerances and allergies
        print("Please answer the following questions about your intolerances and allergies:")
        lactose_intolerant = input("Are you lactose intolerant? (yes/no): ").strip().lower() == 'yes'
        vegan = input("Are you vegan? (yes/no): ").strip().lower() == 'yes'
        gluten_intolerant = input("Are you gluten intolerant? (yes/no): ").strip().lower() == 'yes'

        # Ask for nationality
        nationality = input("Please enter your nationality: ").strip()

        # Retrieve the pantry for the user's nationality
        pantry = self.get_pantry(nationality)

        if not pantry:
            print("Sorry, pantry data for your nationality is not available.")
            return None

        # Display the pantry
        print(f"\nPantry for {nationality}:")
        for category, ingredients in pantry.items():
            print(f"{category}: {', '.join(ingredients)}")

        # Ask about available ingredients
        print("\nLet's check which ingredients you have in your pantry.\n")
        available_ingredients = {}
        for category, ingredients in pantry.items():
            available_ingredients[category] = self.ask_about_ingredients(ingredients)

        # Create the user profile
        user_profile = {
            "nationality": nationality,
            "available_ingredients": available_ingredients,
            "lactose_intolerant": lactose_intolerant,
            "vegan": vegan,
            "gluten_intolerant": gluten_intolerant
        }

        return user_profile


class UserProfileWithIntolerances(UserProfiler):
    """
    A class extending UserProfiler to add allergen and intolerance checks based on user preferences.
    """

    def __init__(self, pantry_path="data/raw/food-pantry.json"):
        super().__init__(pantry_path)

    def filter_food_based_on_user_profile(self, user_profile, food_df):
        """
        Filters food items based on user preferences such as intolerances, allergies, and dietary restrictions.

        :param user_profile: dict containing dietary preferences and allergies
            e.g., {'lactose_intolerant': True, 'vegan': True, 'gluten_intolerant': False, 'allergies': ['Peanuts']}
        :param food_df: DataFrame containing food information with food categories and allergens

        :return: A filtered DataFrame of foods that match the user profile.
        """
        filtered_df = food_df.copy()

        # 1. Lactose intolerant users should not have dairy
        if user_profile.get("lactose_intolerant", False):
            filtered_df = filtered_df[filtered_df["Category Name"] != "Dairy products"]

        # 2. Vegan users should not have dairy, meat, poultry, fish, or seafood
        if user_profile.get("vegan", False):
            filtered_df = filtered_df[filtered_df["Category Name"] != "Dairy products"]
            filtered_df = filtered_df[filtered_df["Category Name"] != "Meat, Poultry"]
            filtered_df = filtered_df[filtered_df["Category Name"] != "Fish, Seafood"]

        # 3. Vegetarian users should exclude meat, poultry, fish, and seafood, but allow dairy
        if user_profile.get("vegetarian", False):
            filtered_df = filtered_df[filtered_df["Category Name"] != "Meat, Poultry"]
            filtered_df = filtered_df[filtered_df["Category Name"] != "Fish, Seafood"]

        # 4. Gluten intolerant users should not have gluten-containing items
        if user_profile.get("gluten_intolerant", False):
            filtered_df = filtered_df[filtered_df["Category Name"] != "Breads, cereals, fastfood,grains"]


        return filtered_df
