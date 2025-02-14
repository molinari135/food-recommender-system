import json
import os
from pathlib import Path
from config import PROCESSED_DATA_PATH


class UserProfiler:
    def __init__(
            self,
            # TODO diet="omnivore",
            intolerances=None,
            food_preferences=None,
            seasonal_preferences=None,
            meals=None,
            used_jolly=False):
        # TODO self.diet = "omnivore"
        self.intolerances = intolerances if intolerances else []
        self.food_preferences = food_preferences if food_preferences else []
        self.seasonal_preferences = seasonal_preferences if seasonal_preferences else []
        self.meals = meals if meals else {}
        self.used_jolly = used_jolly if used_jolly else False

    def set_intolerances(self, intolerance: str):
        """Add an intolerance to the profile"""

        if intolerance == "Lactose":
            self.intolerances.append(["Dairy", "Dairy Breakfast"])
        if intolerance == "Gluten":
            self.intolerances.append(["Grains", "Baked Products", "Baked Products Breakfast"])

    def get_intolerances(self) -> list:
        return self.intolerances

    def set_food_preferences(self, food_list: list):
        """Updates food preferences checking the dataset"""
        # FIXME Do we need to check food_list if data comes from the DataLoader?
        self.food_preferences = food_list

    def get_food_preferences(self) -> list:
        return self.food_preferences

    def set_seasonal_preferences(self, food_list: list):
        """Updates food preferences checking the dataset"""
        self.seasonal_preferences = food_list

    def get_seasonal_preferences(self) -> list:
        return self.seasonal_preferences

    def set_meals(self, meals: dict):
        self.meals = meals

    def get_meals(self) -> dict:
        return self.meals

    def set_used_jolly(self, value: bool):
        self.used_jolly = value

    def get_used_jolly(self) -> bool:
        return self.used_jolly

    def save_profile(self, filename: Path):

        profile_data = {
            # TODO "diet": self.diet,
            "intolerances": self.intolerances,
            "food_preferences": self.food_preferences,
            "seasonal_preferences": self.seasonal_preferences,
            "meals": self.meals,
            "used_jolly": self.used_jolly
        }
        with open(PROCESSED_DATA_PATH / filename, "w") as file:
            json.dump(profile_data, file, indent=4)

    @classmethod
    def check_profile(self, filename: Path):
        """
        Checks if a profile exists for the given filename. If the profile does not exist,
        it creates a new one.

        Args:
            filename (Path): The name of the file to check for the profile.

        Returns:
            None
        """

        if not os.path.exists(PROCESSED_DATA_PATH / filename):
            print("🆕 Profile not found. Creating a new one...")
            self.create_new_profile(filename)

    @classmethod
    def load_profile(cls, filename: Path):

        try:
            with open(PROCESSED_DATA_PATH / filename, "r") as file:
                data = json.load(file)
                return cls(
                    # TODO diet=data["diet"],
                    intolerances=data["intolerances"],
                    food_preferences=data["food_preferences"],
                    seasonal_preferences=data["seasonal_preferences"],
                    meals=data["meals"],
                    used_jolly=data["used_jolly"])
        except FileNotFoundError:
            print("File not found")
            return cls()

    @staticmethod
    def create_new_profile(filename: Path):

        empty_profile = {
            # TODO "diet": "omnivore",
            "intolerances": [],
            "food_preferences": [],
            "seasonal_preferences": [],
            "meals": {},
            "used_jolly": False
        }

        with open(PROCESSED_DATA_PATH / filename, "w") as f:
            json.dump(empty_profile, f, indent=4)

        print(f"🆕 Empty profile created at {PROCESSED_DATA_PATH / filename}")

    def __str__(self) -> str:

        return f"""
            \nDiet: {self.diet},
            \nIntolerances: {self.intolerances},
            \nPreferences: {self.food_preferences},
            \nSeasonal preferences: {self.seasonal_preferences},
            \nMeals: {self.meals}
            \nUsed jolly: {self.used_jolly}
        """
