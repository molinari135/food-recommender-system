import streamlit as st
from food_recommender_system.profiler import UserProfiler
from datetime import datetime
from pathlib import Path
import requests
import os
import pandas as pd
import json


st.set_page_config(
    page_title="Food RecSys - Meals",
    page_icon="🍽️",
)


BASE_PATH = Path(os.path.join(os.getcwd(), 'data'))
RAW_DATA_PATH = Path(os.path.join(BASE_PATH, 'raw'))


with st.sidebar:
    st.page_link('main.py', label='Home')
    st.page_link('pages/1_home.py', label='Create or Load User Profile')
    st.page_link('pages/2_user_profile.py', label='User Profile Information')
    st.page_link('pages/3_meal_selection.py', label='Meal Selection')


food_dataset = pd.read_csv(RAW_DATA_PATH / "nutritional-facts.csv")
food_servings = json.load(open(RAW_DATA_PATH / "food-servings.json", "r"))


def get_current_meal_time():
    current_hour = datetime.now().hour
    if 6 <= current_hour < 10:
        return "Breakfast"
    elif 11 <= current_hour < 15:
        return "Lunch"
    elif 16 <= current_hour < 20:
        return "Dinner"
    else:
        return "Snack"


def get_cheat_meal(fast_food_preferences):
    if not fast_food_preferences:
        st.warning("⚠️ You have not set any fast food preferences.")
        return None

    cheat_request = {"fast_food_preferences": fast_food_preferences}

    try:
        response = requests.post("https://molinari135-food-recsys-api.hf.space/cheat", json=cheat_request)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error fetching cheat meal: {e}")
        return None


def get_user_fast_food_preferences(profile):
    user_preferences = profile.get_food_preferences()
    fast_foods = []

    for food in user_preferences:
        category = food_dataset.loc[food_dataset["Food Name"] == food, "Category Name"]
        if not category.empty and category.values[0] == "Fast Foods":
            fast_foods.append(food)

    return fast_foods


# 🍴 Main function for displaying meal selection
def display_meal_selection():
    if st.session_state.selected_profile == "-- Create a new profile --" or st.session_state.selected_profile is None:
        st.warning("⚠️ No user profile selected. Please create or load a user profile.")
        return

    selected_profile = st.session_state.selected_profile
    profile = UserProfiler.load_profile(Path(selected_profile))

    current_meal_time = get_current_meal_time()
    current_day = datetime.now().weekday()

    meals = profile.get_meals()
    today_meal = meals[current_meal_time][current_day]

    st.subheader(f"📅 Today's {current_meal_time}")

    if len(today_meal) == 3:
        meal, alternative, choice = today_meal

        st.markdown("> **ℹ️ How to read this table**\n> - The first row is the original meal\n> - The second row is the alternative meal\n> - The third row is your choice")

        all_meal_data = []

        for variant in [meal, alternative, choice]:
            row = {}
            for food_name in variant:
                category = food_dataset.loc[
                    food_dataset["Food Name"] == food_name, "Category Name"
                ]
                category_name = category.values[0] if not category.empty else "Unknown"
                row[category_name] = food_name
            all_meal_data.append(row)

        df = pd.DataFrame(all_meal_data).fillna("")
        st.table(df)

        unique_categories = {food_dataset.loc[food_dataset["Food Name"] == food, "Category Name"].values[0]
                             for variant in [meal, alternative, choice]
                             for food in variant if not food_dataset.loc[food_dataset["Food Name"] == food, "Category Name"].empty}

        filtered_food_servings = {category: info for category, info in food_servings.items() if category in unique_categories}

        table_data = [{"Category": category, "Serving Size (grams)": info["serving_size"], "Tips": info["tips"]}
                      for category, info in filtered_food_servings.items()]

        df_nutritional_info = pd.DataFrame(table_data)
        st.markdown("### 🍎 Serving Sizes")
        st.table(df_nutritional_info)

    elif len(today_meal) == 2:
        new_meal = []
        for m, alt in zip(today_meal[0], today_meal[1]):
            choice = st.radio(f"🍽️ Choose between {m} and {alt}", options=[m, alt])
            justification = get_food_justification(m, alt)
            if justification:
                st.markdown(f"ℹ️ {justification[0]['comparison']}")
                st.markdown(f"ℹ️ {justification[0]['persuasion']}")
            new_meal.append(choice)

        if st.button("✅ Confirm meal"):
            updated_meal = (today_meal[0], today_meal[1], new_meal)
            meals[current_meal_time][current_day] = updated_meal
            profile.set_meals(meals)
            profile.save_profile(Path(selected_profile))
            st.success("✅ Meal updated successfully!")
            st.rerun()

    if current_meal_time in ["Lunch", "Dinner"] and profile.used_jolly is False:
        col1, col2 = st.columns([8, 2])
        with col2:
            if st.button("😩 Are you feeling stressed?", help="Click if you had a bad day!"):
                user_fast_foods = get_user_fast_food_preferences(profile)

                if user_fast_foods:
                    cheat_meal = get_cheat_meal(user_fast_foods)

                    fast_food = cheat_meal["chosen_fast_food"] if cheat_meal else None
                    fast_food_alt = cheat_meal["recommended_cheat_meal"][0] if cheat_meal else None

                    if cheat_meal:
                        st.success(f"🍔 Cheat meal granted: {fast_food}")

                        profile.used_jolly = True

                        meals[current_meal_time][current_day] = (
                            [fast_food],
                            [fast_food_alt]
                        )

                        profile.set_meals(meals)
                        profile.save_profile(Path(selected_profile))

                        st.warning("⚠️ Your meal has been updated. Choose your preference below.")
                        st.rerun()
                else:
                    st.warning("⚠️ No fast food preferences found in your selected foods.")


def get_food_justification(meal_1, meal_2):
    data = {"meal_1": [meal_1], "meal_2": [meal_2]}
    response = requests.post("https://molinari135-food-recsys-api.hf.space/justify", json=data)
    if response.status_code == 200:
        return response.json()["justification"]


display_meal_selection()
