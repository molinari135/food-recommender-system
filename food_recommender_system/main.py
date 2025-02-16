from profiler import UserProfiler
from recommender import ask_seasonal_preferences, ask_user_preferences, get_seasonal_food
from dataloader import DataLoader
from mealgen import generate_weekly_meal_plan
from justificator import print_meal, print_full_week_meals, choose_foods_in_current_meal, get_current_meal
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
    print("1. Create or Load User")
    time.sleep(0.5)
    print("2. Display Current Meal and Alternatives")
    time.sleep(0.5)
    print("3. Display Weekly Meal Plan")
    time.sleep(0.5)
    print("4. Learn About Seasonal Food")
    time.sleep(0.5)
    print("0. Exit")
    time.sleep(0.5)


def create_or_load_user():
    name_surname = input("🆔 Enter username to create or load your profile: ").strip().lower()
    filename = Path(f"{name_surname}.json")

    # Check if the profile to load exists, otherwise make a new one and load it
    user_profiler.check_profile(filename)
    user = user_profiler.load_profile(filename)

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
        ask_user_preferences(df, user, filename)
        ask_seasonal_preferences(df, seasonality, user, filename, food_infos)

        generate_weekly_meal_plan(df, servings, user, filename)
    os.system('cls||clear')
    return user, filename


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

    meal_name, current_meal, current_alternative, choosen_meal = get_current_meal(user)

    if choosen_meal:
        print(f"\n🍽️ Today's {meal_name.lower()} is:")
        time.sleep(1)
        print_meal(choosen_meal, df, servings)
        change_meal(user, df, meal_name, filename)
    else:
        print(f"\n🍽️ Today's {meal_name.lower()} is:")
        time.sleep(1)
        print_meal(current_meal, df, servings)
        time.sleep(1)
        print("\n🔄 Alternatively, you can have:")
        time.sleep(1)
        print_meal(current_alternative, df, servings)

        # comparison = compare_meals(df, current_meal, current_alternative)
        # for comp in comparison:
        #     print(comp)
        #     time.sleep(0.5)

        # preferences_df = df[df["Food Name"].isin(user_profiler.get_food_preferences())
        choose_foods_in_current_meal(user, filename, df)
        os.system('cls||clear')


def display_weekly_meal_plan(user):
    print_full_week_meals(user, df, servings)


def learn_about_seasonal_food(food_info: dict):
    """
    Provides information about seasonal foods and allows the user to learn more about each food item.
    Args:
        recsys (RecommenderSystem): An instance of the RecommenderSystem class to get seasonal food data.
        food_info (dict): A dictionary containing detailed information about various foods.
    The function displays the benefits of choosing seasonal produce and lists available seasonal fruits and vegetables.
    The user can select a food item to learn more about its health benefits, how to choose and store it, a description,
    nutritional insights, and additional tips. The user can type 'back' to return to the main menu.
    """
    fruits, vegetables = get_seasonal_food(df, seasonality)
    seasonal_foods = fruits + vegetables

    print("\n🌍 Why choose seasonal produce?")
    time.sleep(1)
    print("✔️  Better taste & freshness – Seasonal foods are naturally ripened and have the best flavor.")
    time.sleep(1)
    print("✔️  Higher nutritional value – Fresh seasonal produce retains more vitamins and minerals.")
    time.sleep(1)
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
            time.sleep(1)
            print(f"💪 Health Benefits: {', '.join(benefits)}\n")
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
            time.sleep(1)
    os.system('cls||clear')


def main():
    try:
        user, filename = create_or_load_user()

        while True:
            show_menu()
            choice = input("Enter your choice (0-4): ")
            os.system('cls||clear')

            if choice == '1':
                user, filename = create_or_load_user()
            elif choice == '2':
                display_current_meal_and_alternatives(user, filename)
            elif choice == '3':
                display_weekly_meal_plan(user)
            elif choice == '4':
                learn_about_seasonal_food(food_infos)
            elif choice == '0':
                print("Exiting the program...")
                time.sleep(1)
                sys.exit(0)
            else:
                print("⚠️ Invalid choice! Please enter a number between 1 and 5.")
                time.sleep(1)

    except Exception as e:
        print(f"🔴 An error occurred: {str(e)}")
        time.sleep(1)


# Run the main function
if __name__ == "__main__":
    main()
