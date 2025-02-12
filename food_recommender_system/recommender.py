import pandas as pd
import json
import numpy as np
from numpy.linalg import norm
from datetime import datetime

from profiler import UserProfiler

EXCLUDED_CATEGORIES = [
    "Baby Foods", "Meals, Entrees, and Side Dishes", "Soups", "Spices", "Fruits", "Vegetables", "Greens"
]

NO_INTOLERANCE_PREFERENCES = {
    "Baked Products": ["Italian bread", "Focaccia, Crackers"],
    "Baked Products Breakfast": ["White Bread, Biscuit"],
    "Beverages": ["Espresso", "Tea", "Orange juice", "Apple juice", "Coffee"],
    "Cured Meat": ["Italian sausage", "Salami", "Mortadella", "Ham"],
    "Dairy": ["Mozzarella", "Ricotta", "Cheese"],
    "Dairy Breakfast": ["Yogurt", "Milk"],
    "Eggs": ["Egg"],
    "Fast Foods": ["Hamburger", "Chicken sandwich", "Pizza"],
    "Gluten-Free Grains": ["Rice"],
    "Grains": ["Pasta", "Wheat Bread"],
    "Lactose-Free Dairy": ["Provolone", "Swiss cheese", "Parmigiano-Reggiano"],
    "Lactose-Free Dairy Breakfast": ["Greek yogurt", "Kefir"],
    "Legumes": ["Chickpeas", "Lentil", "Bean"],
    "Nuts": ["Walnut", "Hazelnut", "Pistachio", "Almond"],
    "Nuts Breakfast": ["Almond paste"],
    "Oils": ["Olive oil"],
    "Red Meat": ["Beef", "Pork"],
    "Sauces": ["Tomato sauce", "Marinara sauce"],
    "Seafood": ["Salmon", "Tuna", "Fish sticks", "Cod", "Mussels"],
    "Sweets": ["Chocolate", "Ice cream"],
    "Sweets Breakfast": ["Marmalade", "Fruit preserves"],
    "White Meat": ["Chicken meat"]
}

NO_DIARY_PREFERENCES = {
    "Baked Products": ["Italian bread", "Focaccia, Crackers"],
    "Baked Products Breakfast": ["White Bread, Biscuit"],
    "Beverages": ["Espresso", "Tea", "Orange juice", "Apple juice", "Coffee"],
    "Cured Meat": ["Italian sausage", "Salami", "Mortadella", "Ham"],
    "Eggs": ["Egg"],
    "Fast Foods": ["Hamburger", "Chicken sandwich", "Pizza"],
    "Gluten-Free Grains": ["Rice"],
    "Grains": ["Pasta", "Wheat Bread"],
    "Lactose-Free Dairy": ["Provolone", "Swiss cheese", "Parmigiano-Reggiano"],
    "Lactose-Free Dairy Breakfast": ["Greek yogurt", "Kefir"],
    "Legumes": ["Chickpeas", "Lentil", "Bean"],
    "Nuts": ["Walnut", "Hazelnut", "Pistachio", "Almond"],
    "Nuts Breakfast": ["Almond paste"],
    "Oils": ["Olive oil"],
    "Red Meat": ["Beef", "Pork"],
    "Sauces": ["Tomato sauce", "Marinara sauce"],
    "Seafood": ["Salmon", "Tuna", "Fish sticks", "Cod", "Mussels"],
    "Sweets": ["Crème caramel", "Chocolate", "Ice cream"],
    "Sweets Breakfast": ["Marmalade", "Fruit preserves"],
    "White Meat": ["Chicken meat"]
}

NO_GRAIN_PREFERENCES = {
    "Beverages": ["Espresso", "Tea", "Orange juice", "Apple juice", "Coffee", "Milk"],
    "Cured Meat": ["Italian sausage", "Salami", "Mortadella", "Ham"],
    "Dairy": ["Mozzarella", "Ricotta", "Cheese"],
    "Dairy Breakfast": ["Yogurt"],
    "Eggs": ["Egg"],
    "Fast Foods": ["Hamburger", "Chicken sandwich", "Pizza"],
    "Gluten-Free Grains": ["Rice"],
    "Lactose-Free Dairy": ["Provolone", "Swiss cheese", "Parmigiano-Reggiano"],
    "Lactose-Free Dairy Breakfast": ["Greek yogurt", "Kefir"],
    "Legumes": ["Chickpeas", "Lentil", "Bean"],
    "Nuts": ["Walnut", "Hazelnut", "Pistachio", "Almond"],
    "Nuts Breakfast": ["Almond paste"],
    "Oils": ["Olive oil"],
    "Red Meat": ["Beef", "Pork"],
    "Sauces": ["Tomato sauce", "Marinara sauce"],
    "Seafood": ["Salmon", "Tuna", "Fish sticks", "Cod", "Mussels"],
    "Sweets": ["Crème caramel", "Chocolate", "Ice cream"],
    "Sweets Breakfast": ["Marmalade", "Fruit preserves"],
    "White Meat": ["Chicken meat"]
}

NO_DIARY_GRAIN_PREFERENCES = {
    "Beverages": ["Espresso", "Tea", "Orange juice", "Apple juice", "Coffee", "Milk"],
    "Cured Meat": ["Italian sausage", "Salami", "Mortadella", "Ham"],
    "Eggs": ["Egg"],
    "Fast Foods": ["Hamburger", "Chicken sandwich", "Pizza"],
    "Gluten-Free Grains": ["Rice"],
    "Lactose-Free Dairy": ["Provolone", "Swiss cheese", "Parmigiano-Reggiano"],
    "Lactose-Free Dairy Breakfast": ["Greek yogurt", "Kefir"],
    "Legumes": ["Chickpeas", "Lentil", "Bean"],
    "Nuts": ["Walnut", "Hazelnut", "Pistachio", "Almond"],
    "Nuts Breakfast": ["Almond paste"],
    "Oils": ["Olive oil"],
    "Red Meat": ["Beef", "Pork"],
    "Sauces": ["Tomato sauce", "Marinara sauce"],
    "Seafood": ["Salmon", "Tuna", "Fish sticks", "Cod", "Mussels"],
    "Sweets": ["Crème caramel", "Chocolate", "Ice cream"],
    "Sweets Breakfast": ["Marmalade", "Fruit preserves"],
    "White Meat": ["Chicken meat"]
}


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
        return df.fillna(fill_value, inplace=True)

    @staticmethod
    def find_nutritional_info(df: pd.DataFrame, food_name: str, only_numbers: bool = True):
        food_info = df[df["Food Name"] == food_name]
        if len(food_info) > 0:
            if only_numbers:
                return food_info.drop(columns=["Food Name", "Category Name"])
            return food_info
        return None

    @staticmethod
    def compute_energy_density(df: pd.DataFrame, food_name: str):
        food_info = DataLoader.find_nutritional_info(df, food_name)
        if isinstance(food_info, str):
            return food_info
        energy_density = food_info["Calories"].values[0] / 100

        if energy_density < 1.5:
            return ("Low", energy_density)
        if 1.5 <= energy_density <= 2.5:
            return ("Medium", energy_density)
        return ("High", energy_density)
    
    @staticmethod
    def find_food_category(df: pd.DataFrame, food_name: str):
        return df[df["Food Name"] == food_name]["Category Name"].values


class RecommenderSystem:
    def __init__(self, df: pd.DataFrame, seasonality: pd.DataFrame, user_profiler: UserProfiler):
        self.df = df
        self.seasonality = seasonality
        self.user_profiler = user_profiler

    def find_seasonal_food(self, nationality: str = "Italy", month: str = ""):
        fruits = []
        vegetables = []

        if not month:
            current_month = datetime.now().strftime("%m")
        else:
            current_month = month

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
    def find_similar_food(df: pd.DataFrame, food_name: str, n: int = 1, same_category: bool = True, low_density_food: bool = True):
        similar_foods = []

        if same_category:
            food_info = DataLoader.find_nutritional_info(df, food_name, only_numbers=False)
            if food_info is None:
                return f"No information found for {food_name}"

            category = food_info["Category Name"].values[0]
            food_A = DataLoader.find_nutritional_info(df, food_name).to_numpy().flatten()

            for food in df[df["Category Name"] == category]["Food Name"]:
                if food == food_name:
                    continue
                food_B = DataLoader.find_nutritional_info(df, food).to_numpy().flatten()

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

    def ask_user_preferences(self):
        preferences = {}
        default_preferences = NO_INTOLERANCE_PREFERENCES

        filtered_df = DataLoader.filter_categories(self.df, EXCLUDED_CATEGORIES)
        categories = filtered_df["Category Name"].unique()
        user_intolerances = self.user_profiler.get_intolerances()

        if user_intolerances is []:
            print("Loading default preferences for no intolerances...")
            default_preferences = NO_INTOLERANCE_PREFERENCES
        if user_intolerances == ["Dairy", "Dairy Breakfast"]:
            print("Loading default preferences for dairy intolerances...")
            default_preferences = NO_DIARY_PREFERENCES
        if user_intolerances == ["Grains", "Baked Products", "Baked Products Breakfast"]:
            print("Loading default preferences for gluten intolerances...")
            default_preferences = NO_GRAIN_PREFERENCES
        if user_intolerances == ["Dairy", "Grains", "Dairy Breakfast", "Baked Products", "Baked Products Breakfast"]:
            print("Loading default preferences for dairy and gluten intolerances...")
            default_preferences = NO_DIARY_GRAIN_PREFERENCES

        data = DataLoader.filter_categories(filtered_df, user_intolerances)
        if user_intolerances == []:
            categories = filtered_df["Category Name"].unique()
        else:
            categories = np.setdiff1d(categories, user_intolerances)

        for category in categories:
            foods = data[data["Category Name"] == category]["Food Name"].tolist()

            print(f"\n{category}:")
            for i, food in enumerate(foods, 1):
                print(f"{i}. {food}")

            while True:
                try:
                    choices = input(f"Select {category} (1-{len(foods)})")
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
        dataset_keys = combined_preferences["Food Name"].unique()
        self.user_profiler.set_food_preferences(food_list, dataset_keys)
        self.user_profiler.save_profile("user_profile.json")

        return combined_preferences.reset_index(drop=True)

    def ask_seasonal_preferences(self):

        # Find seasonal fruits and vegetables
        fruits, vegetables = RecommenderSystem.find_seasonal_food(self)

        # Ask the user for their preferred seasonal fruits and vegetables
        print("Please select your preferred seasonal fruits and vegetables for this month.")
        print("Enter numbers separated by spaces, or press Enter to select all.")

        # Get user preferences for seasonal fruits
        print("\nSeasonal Fruits:")
        for i, fruit in enumerate(fruits, 1):
            print(f"{i}. {fruit}")

        selected_fruits = input(f"Select fruits (1-{len(fruits)}): ").strip()
        if selected_fruits:
            selected_fruits = [fruits[int(i) - 1] for i in selected_fruits.split()]
        else:
            selected_fruits = fruits

        # Get user preferences for seasonal vegetables
        print("\nSeasonal Vegetables:")
        for i, vegetable in enumerate(vegetables, 1):
            print(f"{i}. {vegetable}")

        selected_vegetables = input(f"Select vegetables (1-{len(vegetables)}): ").strip()
        if selected_vegetables:
            selected_vegetables = [vegetables[int(i) - 1] for i in selected_vegetables.split()]
        else:
            selected_vegetables = vegetables

        # Filter the user preferences dataframe to include only selected seasonal fruits and vegetables
        selected_fruits_df = self.df[self.df['Food Name'].isin(selected_fruits)]
        selected_vegetables_df = self.df[self.df['Food Name'].isin(selected_vegetables)]

        # Add breakfast preferences to combined_preferences
        combined_preferences = pd.concat([selected_fruits_df, selected_vegetables_df])

        food_list = combined_preferences["Food Name"].unique()
        dataset_keys = food_list
        self.user_profiler.set_seasonal_preferences(food_list, dataset_keys)
        self.user_profiler.save_profile("user_profile.json")


# user_profiler = UserProfiler()
# user = user_profiler.load_profile("user_profile.json")

# dataloader = DataLoader()
# df = dataloader.load_csv("nutritional-facts.csv")
# seasonality = dataloader.load_json("food-seasonality.json")

# recommender = RecommenderSystem(
#     df=df,
#     seasonality=seasonality,
#     user_profiler=user
# )

# recommender.ask_user_preferences()
# recommender.ask_seasonal_preferences()
