import json


class UserProfiler:
    def __init__(
            self, diet="omnivore",
            intolerances=None,
            food_preferences=None,
            seasonal_preferences=None,
            meals=None,
            used_jolly=False):
        """
        Initialize user profile with diet, intolerances and food preferences.

        :param diet: User's diet (omnivore, vegetarian, vegan)
        :param intolerances: User's intolerances (only dairy, only gluten or both)
        :param food_preferences: List of food names preferences

        ```python
        data = pd.read_csv(r"data\\raw\\nutritional-facts.csv")
        dataset_keys = data["Food Name"].unique()

        # Create a user profile
        user = UserProfiler()
        user.add_intolerance("dairy")
        user.set_food_preferences(["Apple", "Carrot", "Pasta"], dataset_keys)

        # Save the profile
        user.save_profile()

        # Load the profile from the JSON
        new_user = UserProfiler.load_profile()
        print(new_user)

        new_user.set_used_jolly(True)
        print(new_user)
        ```
        """
        self.diet = "omnivore"  # TODO add vegetarian and vegan
        self.intolerances = intolerances if intolerances else []
        self.food_preferences = food_preferences if food_preferences else []
        self.seasonal_preferences = seasonal_preferences if seasonal_preferences else []
        self.meals = meals if meals else {}
        self.used_jolly = used_jolly if used_jolly else False

    def set_intolerances(self, intolerance):
        """Add an intolerance to the profile"""
        if intolerance == "Lactose":
            self.intolerances.append(["Dairy", "Dairy Breakfast"])
        if intolerance == "Gluten":
            self.intolerances.append(["Grains", "Baked Products", "Baked Products Breakfast"])

    def get_intolerances(self):
        return self.intolerances

    def set_food_preferences(self, food_list, dataset_keys):
        """Updates food preferences checking the dataset"""
        valid_preferences = [food for food in food_list if food in dataset_keys]
        self.food_preferences = valid_preferences

    def get_food_preferences(self):
        return self.food_preferences

    def set_seasonal_preferences(self, food_list, dataset_keys):
        """Updates food preferences checking the dataset"""
        valid_preferences = [food for food in food_list if food in dataset_keys]
        self.seasonal_preferences = valid_preferences

    def get_seasonal_preferences(self):
        return self.seasonal_preferences

    def set_meals(self, meals):
        self.meals = meals

    def get_meals(self):
        return self.meals

    def set_used_jolly(self, value):
        """Update the flag, if needed"""
        if value in [True, False]:
            self.used_jolly = value

    def get_used_jolly(self):
        return self.used_jolly

    def save_profile(self, filename="user_profile.json"):
        """Save user profile in a JSON file"""
        profile_data = {
            "diet": self.diet,
            "intolerances": self.intolerances,
            "food_preferences": self.food_preferences,
            "seasonal_preferences": self.seasonal_preferences,
            "meals": self.meals,
            "used_jolly": self.used_jolly
        }
        with open(filename, "w") as file:
            json.dump(profile_data, file, indent=4)

    @classmethod
    def load_profile(cls, filename="user_profile.json"):
        """Load user's profile from JSON file"""
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                return cls(
                    diet=data["diet"],
                    intolerances=data["intolerances"],
                    food_preferences=data["food_preferences"],
                    seasonal_preferences=data["seasonal_preferences"],
                    meals=data["meals"],
                    used_jolly=data["used_jolly"])
        except FileNotFoundError:
            print("File not found")
            return cls()

    @staticmethod
    def create_new_profile(file_path="user_profile.json"):
        empty_profile = {
            "diet": "omnivore",
            "intolerances": [],
            "food_preferences": [],
            "seasonal_preferences": [],
            "meals": {},
            "used_jolly": False
        }

        with open(file_path, "w") as f:
            json.dump(empty_profile, f, indent=4)

        print(f"Empty profile created at {file_path}")

    def __str__(self):
        return f"Diet: {self.diet}, Intolerances: {self.intolerances}, Preferences: {self.food_preferences}, Seasonal preferences: {self.seasonal_preferences}, Meals: {self.meals} Used jolly: {self.used_jolly}"
