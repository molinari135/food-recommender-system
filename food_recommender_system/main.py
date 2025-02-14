from profiler import UserProfiler
from recommender import RecommenderSystem
from dataloader import DataLoader
from mealgen import generate_weekly_meal_plan
from justificator import Justificator
from moodmod import change_meal
from pathlib import Path

import sys
import os
import time


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
    print("\n🍽️ Welcome to the Food Recommender System CLI! 🍽️")
    time.sleep(1)
    print("1️. Create or Load User")
    print("2️. Display Current Meal and Alternatives")
    print("3️. Display Weekly Meal Plan")
    print("4️. Learn About Seasonal Food")
    print("0️. Exit")


def create_or_load_user():
    name_surname = input("🆔 Enter username to create or load your profile: ").strip().lower()
    filename = Path(f"{name_surname}.json")

    # Check if the profile to load exists, otherwise make a new one and load it
    user_profiler.check_profile(filename)
    user = user_profiler.load_profile(filename)

    recsys = RecommenderSystem(df, seasonality, user)

    if user.get_meals() == {} and user.get_intolerances() == []:

        intolerances = input("\n❓ Are you lactose intolerant? (Yes/no): ").strip().lower()
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
    os.system('cls||clear')
    return user, filename, recsys


def display_current_meal_and_alternatives(user: UserProfiler, filename: Path):
    """
    Display the current meal and its alternatives for a given user.
    This function retrieves the current meal and an alternative meal for the user,
    displays the chosen meal if available, or the current meal and its alternative.
    It also compares the current meal with the alternative and prints the comparison.
    Args:
        user (UserProfiler): The user object containing user-specific information.
        filename (Path): The Path where the meal data is stored.
    Returns:
        None
    """
    jst = Justificator(df, seasonality)
    meal_name, current_meal, current_alternative, choosen_meal = Justificator.get_current_meal(user, meal_name="Lunch", debug=True)

    if choosen_meal:
        print(f"\n🍽️ Today's {meal_name.lower()} is:")
        time.sleep(0.5)
        Justificator.print_meal(choosen_meal, df, servings)
        change_meal(user, df, meal_name, filename)
    else:
        print(f"\n🍽️ Today's {meal_name.lower()} is:")
        time.sleep(0.5)
        Justificator.print_meal(current_meal, df, servings)
        print("\n🔄 Alternatively, you can have:")
        Justificator.print_meal(current_alternative, df, servings)

        comparison = jst.compare_meals(current_meal, current_alternative)
        for comp in comparison:
            print(comp)

        # preferences_df = df[df["Food Name"].isin(user_profiler.get_food_preferences())
        Justificator.choose_foods_in_current_meal(user, filename)


def display_weekly_meal_plan(user):
    Justificator.print_full_week_meals(user, df, servings)


def learn_about_seasonal_food(recsys: RecommenderSystem, food_info: dict):
    """
    Provides information about seasonal foods and allows the user to learn more about each food item.
    Args:
        recsys (RecommenderSystem): An instance of the RecommenderSystem class to get seasonal food data.
        food_info (dict): A dictionary containing detailed information about various foods.
    The function displays the benefits of choosing seasonal produce and lists available seasonal fruits and vegetables.
    The user can select a food item to learn more about its health benefits, how to choose and store it, a description,
    nutritional insights, and additional tips. The user can type 'back' to return to the main menu.
    """
    fruits, vegetables = recsys.get_seasonal_food()
    seasonal_foods = fruits + vegetables

    print("\n🌍 Why choose seasonal produce?")
    time.sleep(0.5)
    print("✔️  Better taste & freshness – Seasonal foods are naturally ripened and have the best flavor.")
    print("✔️  Higher nutritional value – Fresh seasonal produce retains more vitamins and minerals.")
    print("✔️  Lower environmental impact – Locally grown seasonal food reduces transportation emissions.")

    time.sleep(2)

    print("\n🌞 Select a seasonal food to learn more or type 'back' to return to the main menu:")
    time.sleep(1)

    for idx, food in enumerate(seasonal_foods, start=1):
        print(f"{idx}. {food}")
        time.sleep(0.5)

    while True:

        print("\n🌞 Select a seasonal food to learn more or type 'back' to return to the main menu:")
        choice = input("Enter your choice: ").strip().lower()

        if choice == 'back':
            break

        if choice.isdigit() and 1 <= int(choice) <= len(seasonal_foods):
            food = seasonal_foods[int(choice) - 1]
            benefits = food_info.get(food, {}).get("benefits", "No information available")
            how_to_choose = food_info.get(food, {}).get("how_to_choose", "No information available")
            how_to_store = food_info.get(food, {}).get("how_to_store", "No information available")
            description = food_info.get(food, {}).get("description", "No information available")
            nutritional_intake = food_info.get(food, {}).get("nutritional_intake", "No information available")
            tips = food_info.get(food, {}).get("tips", "No tips available")

            print(f"\n📌 {food.upper()}")
            print(f"💪 Health Benefits: {", ".join(benefits)}\n")
            time.sleep(1)
            print(f"🛒 How to Choose: {how_to_choose}")
            time.sleep(1)
            print(f"❄️  How to Store: {how_to_store}\n")
            time.sleep(1)
            print(f"📌 Description: {description}")
            time.sleep(1)
            print(f"🥗 Nutritional Insights: {nutritional_intake}\n")
            time.sleep(1)
            print(f"💡 Tips: {tips}")
            time.sleep(3)

        else:
            print("⚠️ Invalid choice! Please enter a valid number or 'back'.")


def main():
    try:
        user, filename, recsys = create_or_load_user()

        while True:
            show_menu()
            choice = input("Enter your choice (0-4): ")
            os.system('cls||clear')

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
                print("⚠️ Invalid choice! Please enter a number between 1 and 5.")

    except Exception as e:
        print(f"🔴 An error occurred: {str(e)}")


# Run the main function
if __name__ == "__main__":
    main()
