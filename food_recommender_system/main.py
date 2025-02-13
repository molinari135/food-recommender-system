from profiler import UserProfiler
from recommender import RecommenderSystem
from dataloader import DataLoader
from mealgen import generate_weekly_meal_plan
from justificator import Justificator
from moodmod import change_meal
from pathlib import Path

import sys


user_profiler = UserProfiler()
dataloader = DataLoader()

nutritional_facts_file = Path("nutritional-facts.csv")
food_seasonality_file = Path("food-seasonality.json")
servings_file = Path("food-servings.json")
fast_food_eqiv_file = Path("fast-food-equiv.json")
food_infos_file = Path("food-infos.json")

df = dataloader.load_csv(nutritional_facts_file)
seasonality = dataloader.load_json(food_seasonality_file)
servings = dataloader.load_json(servings_file)
fast_food_equiv = dataloader.load_json(fast_food_eqiv_file)
food_infos = dataloader.load_json(food_infos_file)


def show_menu():
    print("\nWelcome to the Food Recommender System CLI!")
    print("1. Create or Load User")
    print("2. Display Current Meal and Alternatives")
    print("3. Display Weekly Meal Plan")
    print("4. Learn About Seasonal Food")
    print("0. Exit")


def create_or_load_user():
    name_surname = input("Enter username to create or load your profile: ").strip().lower()
    filename = Path(f"{name_surname}.json")

    # Check if the profile to load exists, otherwise make a new one and load it
    user_profiler.check_profile(filename)
    user = user_profiler.load_profile(filename)

    recsys = RecommenderSystem(df, seasonality, user)

    if user.get_meals() == {} and user.get_intolerances() == []:

        intolerances = input("Are you lactose intolerant? (Yes/no): ").strip().lower()
        if intolerances == "yes":
            user.set_intolerances("Lactose")

        # FIXME actually not working!
        # intolerances = input("Are you gluten intolerant? (Yes/no): ").strip().lower()
        # if intolerances == "yes":
        #     user.set_intolerances("Gluten")

        # Save the profile
        user.save_profile(filename)
        recsys.ask_user_preferences(filename)
        recsys.ask_seasonal_preferences(filename, food_infos)

        generate_weekly_meal_plan(df, servings, user, filename)

    return user, filename, recsys

def display_current_meal_and_alternatives(user, filename):
    jst = Justificator(df, seasonality)
    meal_name, current_meal, current_alternative = Justificator.get_current_meal(user, df)
    
    print(f"\nToday's {meal_name.lower()} is:")
    Justificator.print_meal(current_meal, df, servings)
    print("\nAlternatively, you can have:")
    Justificator.print_meal(current_alternative, df, servings)

    comparison = jst.compare_meals(current_meal, current_alternative)
    for comp in comparison:
        print(comp)

    # preferences_df = df[df["Food Name"].isin(user_profiler.get_food_preferences())]
    change_meal(user, df, fast_food_equiv, meal_name, servings, filename)


def display_weekly_meal_plan(user):
    Justificator.print_full_week_meals(user, df, servings)


def learn_about_seasonal_food(recsys: RecommenderSystem, food_info: dict):
    fruits, vegetables = recsys.get_seasonal_food()

    print("\nHere are some tips for your selected foods:")
    for food in fruits + vegetables:
        how_to_choose = food_info.get(food, {}).get("how_to_choose", "No information available")
        how_to_store = food_info.get(food, {}).get("how_to_store", "No information available")
        tips = food_info.get(food, {}).get("tips", "No tips available")

        print(f"\n📌 {food.upper()}")
        print(f"🛒 How to Choose: {how_to_choose}")
        print(f"❄️ How to Store: {how_to_store}")
        print(f"💡 Tips: {tips}")


def main():
    try:
        user, filename, recsys = create_or_load_user()
        
        while True:
            show_menu()
            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                user, filename, recsys = create_or_load_user()
            elif choice == '2':
                display_current_meal_and_alternatives(user, filename)
            elif choice == '3':
                display_weekly_meal_plan(user)
            elif choice == '4':
                learn_about_seasonal_food(recsys, food_infos)
            elif choice == '0':
                print("Exiting the program...")
                sys.exit(0)
            else:
                print("Invalid choice! Please enter a number between 1 and 5.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Run the main function
if __name__ == "__main__":
    main()
