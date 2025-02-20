import streamlit as st
from food_recommender_system.profiler import UserProfiler
from datetime import datetime
from pathlib import Path
import requests
import os
import pandas as pd
import json


st.set_page_config(
    page_title="Food RecSys - Meals",  # Change tab title
    page_icon="🍽️",  # Change favicon (can be an emoji or URL to an image)
)


BASE_PATH = Path(os.path.join(os.getcwd(), 'data'))
RAW_DATA_PATH = Path(os.path.join(BASE_PATH, 'raw'))


with st.sidebar:
    st.page_link('pages/1_home.py', label='Create or Load User Profile')
    st.page_link('pages/2_user_profile.py', label='User Profile Information')
    st.page_link('pages/3_meal_selection.py', label='Meal Selection')


food_dataset = pd.read_csv(RAW_DATA_PATH / "nutritional-facts.csv")
food_servings = json.load(open(RAW_DATA_PATH / "food-servings.json", "r"))


# Function to get the current meal time based on the system clock
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


# Main function for displaying meal selection
def display_meal_selection():
    if st.session_state.selected_profile == "-- Create a new profile --" or "selected_profile" not in st.session_state:
        st.warning("No user profile selected. Please create or load a user profile.")
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

        st.markdown("> How to read this table\n> - The first row is the original meal\n> - The second row is the alternative meal\n> - The third row is your choice")

        # For displaying the meal variants table in a similar manner as above
        all_meal_data = []

        # Loop over meal variants (different options for the meal)
        for variant in [meal, alternative, choice]:  # Assuming meal, alternative, and choice are lists of food items
            row = {}

            # Process each food item
            for food_name in variant:
                category = food_dataset.loc[
                    food_dataset["Food Name"] == food_name, "Category Name"
                ]
                category_name = category.values[0] if not category.empty else "Unknown"

                # Store the food item under its category
                row[category_name] = food_name

            all_meal_data.append(row)

        # Convert the list to a DataFrame
        df = pd.DataFrame(all_meal_data).fillna("")  # Fill empty values for display

        # Display the meal variants table
        st.table(df)

        # Extract unique categories from today's meal
        unique_categories = set()
        for variant in [meal, alternative, choice]:
            for food_name in variant:
                category = food_dataset.loc[
                    food_dataset["Food Name"] == food_name, "Category Name"
                ]
                category_name = category.values[0] if not category.empty else "Unknown"
                unique_categories.add(category_name)

        # Filter food_servings to only include the categories present in today's meal
        filtered_food_servings = {category: info for category, info in food_servings.items() if category in unique_categories}

        # Create an empty list to hold the rows of the table for nutritional information
        table_data = []

        # Loop through the filtered food_servings dictionary to collect the nutritional details
        for category, info in filtered_food_servings.items():
            row = {
                "Category": category,
                "Serving Size (grams)": info["serving_size"],
                "Tips": info["tips"]
            }
            table_data.append(row)

        # Convert the list to a DataFrame
        df_nutritional_info = pd.DataFrame(table_data)

        # Display the nutritional information table
        st.markdown("### 🍎 Serving Sizes")
        st.table(df_nutritional_info)

    elif len(today_meal) == 2:
        new_meal = []
        for m, alt in zip(today_meal[0], today_meal[1]):
            choice = st.radio(f"Choose between {m} and {alt}", options=[m, alt])
            justification = get_food_justification(m, alt)[0]
            st.markdown(f"{justification['comparison']}")
            st.markdown(f"{justification['persuasion']}")
            new_meal.append(choice)

        if st.button("Confirm meal"):
            updated_meal = (today_meal[0], today_meal[1], new_meal)
            meals[current_meal_time][current_day] = updated_meal
            profile.set_meals(meals)
            profile.save_profile(Path(selected_profile))
            st.success("Meal updated successfully!")
            st.rerun()


# Call the function to display the meal selection
def get_food_justification(meal_1, meal_2):
    data = {"meal_1": [meal_1], "meal_2": [meal_2]}
    response = requests.post("https://molinari135-food-recsys-api.hf.space/justify", json=data)
    if response.status_code == 200:
        return response.json()["justification"]


display_meal_selection()
