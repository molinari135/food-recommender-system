import numpy as np
from recommender import DataLoader


class Justificator:
    """Provides explanations about fruits, vegetables, and meal choices based on nutritional data."""

    def __init__(self, nutrition_data_path="nutritional-facts.csv", seasonal_info_path="food-infos.json"):
        """Loads the nutritional database."""
        self.dataloader = DataLoader()
        self.df = self.dataloader.load_csv(nutrition_data_path)
        self.seasonal_info = self.dataloader.load_json(seasonal_info_path)
        self.macronutrients = ["Calories", "Carbs", "Fats", "Fiber", "Protein"]

    def compare_meals(self, meal1, meal2):
        """
        Compares each food in meal1 with the corresponding food in meal2 for macronutrient values.

        Args:
            meal1 (list): List of food items in the first meal.
            meal2 (list): List of food items in the second meal.

        Returns:
            str: A detailed comparison for each macronutrient.
        """
        if len(meal1) != len(meal2):
            return "Error: The two meals should have the same number of items for a fair comparison."

        comparison_results = []

        for food1, food2 in zip(meal1, meal2):
            food1_info = self.dataloader.find_nutritional_info(self.df, food1, only_numbers=False)
            food2_info = self.dataloader.find_nutritional_info(self.df, food2, only_numbers=False)

            if food1_info.size == 0 or food2_info.size == 0:
                return f"Error: Nutritional information for '{food1}' or '{food2}' is missing."

            comparison = f"**Comparing {food1} vs {food2}:**\n"

            food1_info = np.array(food1_info[self.macronutrients])[0]
            food2_info = np.array(food2_info[self.macronutrients])[0]

            # print(food1_info[0])

            comparison = f"Comparing {food1} vs {food2}:\n"
            persuasion = "💡 Which one should you choose?\n"

            better_choice = {"food": None, "score": 0}  # Track which food is better based on nutrition

            for i, nutrient in enumerate(self.macronutrients):
                f1_value, f2_value = float(food1_info[i]), float(food2_info[i])

                if f1_value < f2_value:
                    comparison += f"- {nutrient}: {food1} has less ({int(f1_value)}), {food2} has more ({int(f2_value)}).\n"
                    if nutrient in ["Calories", "Carbs", "Fats"]:
                        better_choice["food"] = food1  # Lower calories/carbs/fats = usually healthier
                        better_choice["score"] += 1
                elif f1_value > f2_value:
                    comparison += f"- {nutrient}: {food1} has more ({int(f1_value)}), {food2} has less ({int(f2_value)}).\n"
                    if nutrient in ["Protein", "Fiber"]:
                        better_choice["food"] = food1  # More protein/fiber = usually healthier
                        better_choice["score"] += 1
                else:
                    comparison += f"- {nutrient}: Both have the same amount ({f1_value}).\n"

            # Persuasion logic
            if better_choice["food"]:
                if better_choice["food"] == food1:
                    persuasion += f"👉 {food1} seems like the healthier choice as it has better macronutrient balance.\n"
                else:
                    persuasion += f"👉 **{food2} is a better option** if you're looking for a healthier alternative.\n"

            # Additional tailored reasoning
            if food1_info[0] < food2_info[0]:  # Lower calories is generally healthier
                persuasion += f"🔥 If you're trying to lose weight, {food1} is a lighter choice.\n"
            if food1_info[3] > food2_info[3]:  # More fiber is better for digestion
                persuasion += f"🌿 {food1} has more fiber, making it better for digestion and gut health.\n"
            if food1_info[4] > food2_info[4]:  # More protein helps with muscle growth
                persuasion += f"💪 If you're looking to build muscle, {food1} is the better option.\n"

            # Balanced advice
            persuasion += "😋 Or simply... follow your taste!\n"

            comparison_results.append(comparison + "\n" + persuasion)

        return comparison_results

    def recommend_fruit_or_vegetable(self, food_name):
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
        recommendation += f"💪 Health Benefits: {', '.join(details['benefits'])}\n"
        # recommendation += f"🛒 How to Choose: {details['how_to_choose']}\n"
        # recommendation += f"❄️ How to Store: {details['hot_to_store']}\n"
        recommendation += f"🥗 Nutritional Insights: {details['nutritional_intake']}\n"

        # Persuasive reasoning for seasonality
        recommendation += "\n🌍 Why choose seasonal produce?\n"
        recommendation += "✔️ Better taste & freshness – Seasonal foods are naturally ripened and have the best flavor.\n"
        recommendation += "✔️ Higher nutritional value – Fresh seasonal produce retains more vitamins and minerals.\n"
        recommendation += "✔️ Lower environmental impact – Locally grown seasonal food reduces transportation emissions.\n"

        # recommendation += "\n🍽️ Pro Tip: " + details["tips"] + "\n"

        return recommendation


# # Example usage
# if __name__ == "__main__":
#     justificator = Justificator()

#     # Example: Comparing two meals
#     meal1 = ["Rice", "Tuna", "Olive oil", "Tomato sauce", "Artichoke", "Pear"]
#     meal2 = ["Pasta", "Bean", "Olive oil", "Marinara sauce", "Pumpkin", "Kiwifruit"]
#     justif = justificator.compare_meals(meal1, meal2)
#     justifruit = justificator.recommend_fruit_or_vegetable(meal1[5])

#     print(justif[1])
#     print(justifruit)
