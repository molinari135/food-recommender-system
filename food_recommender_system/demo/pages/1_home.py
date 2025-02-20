import streamlit as st
from food_recommender_system.profiler import UserProfiler
from pathlib import Path
import os
import requests
import json
from datetime import datetime
import time
import pandas as pd

st.set_page_config(
    page_title="Food RecSys - Home",  # Change tab title
    page_icon="🍽️",  # Change favicon (can be an emoji or URL to an image)
)

# Paths and dataset setup
BASE_PATH = Path(os.path.join(os.getcwd(), 'data'))
RAW_DATA_PATH = Path(os.path.join(BASE_PATH, 'raw'))
PROCESSED_DATA_PATH = Path(os.path.join(BASE_PATH, 'processed'))

EXCLUDED_CATEGORIES = ["Baby Foods", "Meals, Entrees, and Side Dishes", "Soups", "Spices", "Greens"]

food_dataset = pd.read_csv(RAW_DATA_PATH / "nutritional-facts.csv")
food_dataset = food_dataset[~food_dataset['Category Name'].isin(EXCLUDED_CATEGORIES)]
food_seasonality = json.load(open(RAW_DATA_PATH / "food-seasonality.json", "r"))

st.session_state.food_dataset = food_dataset
st.session_state.food_seasonality = food_seasonality

with st.sidebar:
    st.page_link('main.py', label='Home')
    st.page_link('pages/1_home.py', label='Create or Load User Profile')
    st.page_link('pages/2_user_profile.py', label='User Profile Information')
    st.page_link('pages/3_meal_selection.py', label='Meal Selection')


# Load profiles
def load_profiles():
    profiles = []
    for filename in os.listdir(PROCESSED_DATA_PATH):
        if filename.endswith(".json"):
            profiles.append(filename)
    return profiles


def categorize_foods():
    seasonal_foods = get_seasonal_foods()

    seasonal = []
    non_seasonal = []

    # Categorize foods
    for _, row in food_dataset.iterrows():
        food_name = row['Food Name']
        if food_name in seasonal_foods:
            seasonal.append(food_name)
        else:
            non_seasonal.append(food_name)

    return seasonal, non_seasonal


def get_seasonal_foods():
    current_month = datetime.now().strftime("%m")  # e.g., "02" for February
    seasonal_data = food_seasonality
    country_data = seasonal_data.get("Italy")  # Adjust for your region if necessary
    seasonal_foods = country_data.get(current_month, [])
    return seasonal_foods


# Main function to load or create user profile
def load_user_profile():
    profiles = load_profiles()

    # Ensure session state for selected profile
    if st.session_state.selected_profile is None:
        st.session_state.selected_profile = "-- Create a new profile --"

    selected_profile = st.selectbox("📂 Select an existing profile", ["-- Create a new profile --"] + profiles)

    if selected_profile != "-- Create a new profile --":
        st.session_state.selected_profile = selected_profile
        st.success(f"✅ Selected profile: {selected_profile}")
        st.switch_page("pages/2_user_profile.py")
    else:
        # Create a new profile
        st.subheader("🆕 Create a new profile")
        new_profile = UserProfiler()
        df = food_dataset.copy()

        name = st.text_input("👤 Enter your name:")
        lactose_intolerance = st.selectbox("🥛 Do you have lactose intolerance?", options=["No", "Yes"])

        if lactose_intolerance == "Yes":
            df = df[~df['Category Name'].isin(['Dairy', 'Dairy Breakfast'])]

        seasonal_foods, _ = categorize_foods()

        # Dictionary to hold user selections for each category
        user_preferences = {}
        categories = df["Category Name"].unique().tolist()
        if lactose_intolerance == "Yes":
            categories = [category for category in categories if category not in ['Dairy', 'Dairy Breakfast']]
        category_foods = {category: df[df["Category Name"] == category]["Food Name"].tolist() for category in categories}

        # For each category, ask the user to select foods
        for category, foods in category_foods.items():
            # Pre-fill multiselect with all foods by default
            selected_foods = st.multiselect(
                f"🍽️ Select your preferred {category} (remove the ones you don't like)",
                options=foods,
                default=foods  # Pre-selected by default
            )

            # Ensure at least one food remains selected
            if not selected_foods:
                st.warning(f"⚠️ You must select at least one food in {category}. Defaulting to the first item.")
                selected_foods = [foods[0]]  # Restore at least one default food

            user_preferences[category] = selected_foods

        # Now, categorize the selected foods into seasonal and non-seasonal
        seasonal_preferences = []
        non_seasonal_preferences = []

        for category, selected_foods in user_preferences.items():
            for food in selected_foods:
                if food in seasonal_foods:
                    seasonal_preferences.append(food)
                elif category not in ["Fruits", "Vegetables"]:
                    non_seasonal_preferences.append(food)

        # Create and save the new profile
        if st.button("💾 Create Profile"):
            new_profile.set_intolerances("Lactose" if lactose_intolerance == "Yes" else [])
            new_profile.set_food_preferences(non_seasonal_preferences)
            new_profile.set_seasonal_preferences(seasonal_preferences)
            new_profile.set_used_jolly(False)

            user_data = {
                "food_preferences": new_profile.get_food_preferences(),
                "seasonal_preferences": new_profile.get_seasonal_preferences(),
                "intolerances": new_profile.get_intolerances()[0] if new_profile.get_intolerances() else None
            }

            meals = {}

            try:
                response = requests.post("https://molinari135-food-recsys-api.hf.space/generate", json=user_data)
                response.raise_for_status()  # Raise an error for bad responses
                meals = response.json()["meals"]
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Error generating meals: {e}")

            new_profile.set_meals(meals)

            filename = f"{name.replace(' ', '_').lower()}.json"
            new_profile.save_profile(PROCESSED_DATA_PATH / filename)

            st.session_state.selected_profile = filename
            st.success(f"🎉 Profile '{filename}' created successfully!")
            time.sleep(1)
            st.switch_page("pages/2_user_profile.py")


load_user_profile()
