from profiler import UserProfiler
from recommender import RecommenderSystem
from dataloader import DataLoader
from mealgen import generate_weekly_meal_plan
from justificator import Justificator
from moodmod import change_meal
from pathlib import Path


# Main process
def main():
    try:
        user_profiler = UserProfiler()
        dataloader = DataLoader()

        nutritional_facts_file = Path("nutritional-facts.csv")
        food_seasonality_file = Path("food-seasonality.json")
        servings_file = Path("food-servings.json")
        fast_food_eqiv_file = Path("fast-food-equiv.json")

        df = dataloader.load_csv(nutritional_facts_file)
        seasonality = dataloader.load_json(food_seasonality_file)
        servings = dataloader.load_json(servings_file)
        fast_food_equiv = dataloader.load_json(fast_food_eqiv_file)

        name_surname = input("Enter name_surname to create or load your profile: ").strip().lower()
        filename = Path(f"{name_surname}.json")

        # Check if the profile to load exists, otherwise make a new one and load it
        user_profiler.check_profile(filename)
        user = user_profiler.load_profile(filename)

        recommender = RecommenderSystem(df, seasonality, user)
        justificator = Justificator(df, seasonality)

        if user.get_meals() == {} and user.get_intolerances() == []:

            intolerances = input("Are you lactose intolerant? (Yes/no): ").strip().lower()
            if intolerances == "yes":
                user.set_intolerances("Lactose")

            intolerances = input("Are you gluten intolerant? (Yes/no): ").strip().lower()
            if intolerances == "yes":
                user.set_intolerances("Gluten")

            # Save the profile
            user.save_profile(filename)
            recommender.ask_user_preferences(filename)
            recommender.ask_seasonal_preferences(filename)

            generate_weekly_meal_plan(df, servings, user, filename)

        meal_name, current_meal, current_alternative = Justificator.get_current_meal(user, df)

        # Justificator.print_full_week_meals(user, df, servings)

        print(f"\nToday's {meal_name.lower()} is:")
        Justificator.print_meal(current_meal, df, servings)
        print("\nAlternatively, you can have:")
        Justificator.print_meal(current_alternative, df, servings)

        comparison = justificator.compare_meals(current_meal, current_alternative)
        for comp in comparison:
            print(comp)

        preferences_df = df[df["Food Name"].isin(user_profiler.get_food_preferences())]
        change_meal(user, preferences_df, fast_food_equiv, meal_name, filename)

    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Run the main function
if __name__ == "__main__":
    main()
