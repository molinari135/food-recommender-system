import streamlit as st
from food_recommender_system.profiler import UserProfiler
import requests
import time
import food_recommender_system.demo.main as main

# Set the page configuration
st.set_page_config(
    page_title="Food RecSys - Home",
    page_icon="👤",
)

# Paths and dataset setup
BASE_PATH = st.session_state.BASE_PATH
RAW_DATA_PATH = st.session_state.RAW_DATA_PATH
PROCESSED_DATA_PATH = st.session_state.PROCESSED_DATA_PATH
EXCLUDED_CATEGORIES = st.session_state.EXCLUDED_CATEGORIES
food_dataset = st.session_state.food_dataset
food_seasonality = st.session_state.food_seasonality

# Sidebar navigation
with st.sidebar:
    st.page_link('main.py', label='🏠 Home')
    st.page_link('pages/1_home.py', label='👤 Create or Load User Profile')
    st.page_link('pages/2_user_profile.py', label='📋 User Profile Information')
    st.page_link('pages/3_meal_selection.py', label='🍽️ Meal Selection')


def load_user_profile():
    """
    Main function to load or create a user profile.
    """
    profiles = main.load_profiles()

    # Ensure session state for selected profile
    if st.session_state.selected_profile is None:
        st.session_state.selected_profile = "-- Create a new profile --"

    st.title("👤 Create or Load User Profile")
    st.markdown("---")
    st.subheader("Select an existing profile")
    selected_profile = st.selectbox("📂 Select an existing profile", ["-- Create a new profile --"] + profiles)

    if selected_profile != "-- Create a new profile --":
        st.session_state.selected_profile = selected_profile
        st.success(f"✅ Selected profile: {selected_profile}")
        st.switch_page("pages/2_user_profile.py")
    else:
        create_new_profile()


def create_new_profile():
    """
    Function to create a new user profile.
    """
    new_profile = UserProfiler()
    df = food_dataset.copy()

    st.markdown("---")
    st.subheader("Create a new profile")
    name = st.text_input("👤 Enter your name to create a new profile:")
    lactose_intolerance = st.selectbox("🥛 Do you have lactose intolerance?", options=["No", "Yes"])

    if lactose_intolerance == "Yes":
        df = df[~df['Category Name'].isin(['Dairy', 'Dairy Breakfast'])]

    seasonal_foods, _ = main.categorize_foods()

    # Dictionary to hold user selections for each category
    user_preferences = get_user_preferences(df, lactose_intolerance)

    # Categorize the selected foods into seasonal and non-seasonal
    seasonal_preferences, non_seasonal_preferences = categorize_preferences(user_preferences, seasonal_foods)

    # Create and save the new profile
    if st.button("💾 Create Profile"):
        save_new_profile(new_profile, name, lactose_intolerance, non_seasonal_preferences, seasonal_preferences)


def get_user_preferences(df, lactose_intolerance):
    """
    Get user preferences for each food category.
    """
    user_preferences = {}
    categories = df["Category Name"].unique().tolist()
    if lactose_intolerance == "Yes":
        categories = [category for category in categories if category not in ['Dairy', 'Dairy Breakfast']]
    category_foods = {category: df[df["Category Name"] == category]["Food Name"].tolist() for category in categories}

    for category, foods in category_foods.items():
        selected_foods = st.multiselect(
            f"🍽️ Select your preferred {category} (remove the ones you don't like)",
            options=foods,
            default=foods
        )

        if not selected_foods:
            st.warning(f"⚠️ You must select at least one food in {category}. Defaulting to the first item.")
            selected_foods = [foods[0]]

        user_preferences[category] = selected_foods

    return user_preferences


def categorize_preferences(user_preferences, seasonal_foods):
    """
    Categorize the selected foods into seasonal and non-seasonal.
    """
    seasonal_preferences = []
    non_seasonal_preferences = []

    for category, selected_foods in user_preferences.items():
        for food in selected_foods:
            if food in seasonal_foods:
                seasonal_preferences.append(food)
            elif category not in ["Fruits", "Vegetables"]:
                non_seasonal_preferences.append(food)

    return seasonal_preferences, non_seasonal_preferences


def save_new_profile(new_profile, name, lactose_intolerance, non_seasonal_preferences, seasonal_preferences):
    """
    Save the new user profile.
    """
    with st.spinner("Creating profile..."):
        new_profile.set_intolerances("Lactose" if lactose_intolerance == "Yes" else [])
        new_profile.set_food_preferences(non_seasonal_preferences)
        new_profile.set_seasonal_preferences(seasonal_preferences)
        new_profile.set_used_jolly(False)

        user_data = {
            "food_preferences": new_profile.get_food_preferences(),
            "seasonal_preferences": new_profile.get_seasonal_preferences(),
            "intolerances": new_profile.get_intolerances()[0] if new_profile.get_intolerances() else None
        }

        meals = generate_meals(user_data)
        new_profile.set_meals(meals)

        filename = f"{name.replace(' ', '_').lower()}.json"
        new_profile.save_profile(PROCESSED_DATA_PATH / filename)

        st.session_state.selected_profile = filename
        st.success(f"🎉 Profile '{filename}' created successfully!")
        time.sleep(1)
        st.switch_page("pages/2_user_profile.py")


def generate_meals(user_data):
    """
    Generate meals based on user data.
    """
    try:
        response = requests.post("https://molinari135-food-recsys-api.hf.space/generate", json=user_data)
        response.raise_for_status()
        return response.json()["meals"]
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error generating meals: {e}")
        return {}


# Load or create user profile
load_user_profile()
