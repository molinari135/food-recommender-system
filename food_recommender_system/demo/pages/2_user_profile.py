import streamlit as st
from food_recommender_system.profiler import UserProfiler
from pathlib import Path
import pandas as pd
import time

# Set the page configuration
st.set_page_config(
    page_title="Food RecSys - User Profile",
    page_icon="📋",
)

# Constants for paths
BASE_PATH = st.session_state.BASE_PATH
RAW_DATA_PATH = st.session_state.RAW_DATA_PATH

# Sidebar navigation
with st.sidebar:
    st.page_link('main.py', label='🏠 Home')
    st.page_link('pages/1_home.py', label='👤 Create or Load User Profile')
    st.page_link('pages/2_user_profile.py', label='📋 User Profile Information')
    st.page_link('pages/3_meal_selection.py', label='🍽️ Meal Selection')

# Load session state data
food_dataset = st.session_state.food_dataset
food_infos = st.session_state.food_infos


def display_user_profile():
    """
    Main function for displaying user profile information.
    """
    if st.session_state.selected_profile == "-- Create a new profile --" or st.session_state.selected_profile is None:
        st.warning("⚠️ No user profile selected. Please create or load a user profile.")
        return

    selected_profile = st.session_state.selected_profile
    profile = UserProfiler.load_profile(Path(selected_profile))
    profile_name = selected_profile[:-5].replace('_', ' ').capitalize()

    st.title(f"👋 Welcome, {profile_name}!")

    display_additional_information(profile)
    display_meals(profile)
    display_seasonal_information(profile)


def display_additional_information(profile):
    """
    Display additional information such as intolerances and jolly meal usage.
    """
    with st.expander("📋 Additional Information"):
        intolerances = profile.get_intolerances()
        if intolerances and intolerances[0]:
            st.markdown("Intolerances: " + ", ".join(intolerances[0]))
        else:
            st.markdown("No intolerances listed.")

        used_jolly = profile.get_used_jolly()
        st.markdown("Your Jolly Meal has been used for this week!" if used_jolly else "Your Jolly Meal has not been used for this week.")


def display_meals(profile):
    """
    Display the meal plan for the week.
    """
    st.subheader("🥗 Meals")
    st.markdown("This is your meal plan for the week. You can view the meals for each day by expanding the section below. Remember that snacks can be eaten **twice a day**!")
    st.markdown("> You can also **print** this page for easy reference by clicking on the three dots on the top right after expanding all sections.")
    
    meals = profile.get_meals()
    if "Snack" in meals:
        meals["Snack"] = meals["Snack"][:7]

    if meals:
        for meal_time, meal_options in meals.items():
            with st.expander(f"**{meal_time.capitalize()}** ({len(meal_options)} days)"):
                for day_index, meal_variants in enumerate(meal_options):
                    st.markdown(f"#### 📅 Day {day_index + 1}")
                    display_meal_variants(meal_variants)
    else:
        st.write("📋 No meals available.")


def display_meal_variants(meal_variants):
    """
    Display meal variants for a specific day.
    """
    all_meal_data = []
    for variant in meal_variants:
        row = {}
        for food_name in variant:
            category = food_dataset[food_dataset["Food Name"] == food_name]["Category Name"]
            category_name = category.values[0] if not category.empty else "Unknown"
            row[category_name] = food_name
        all_meal_data.append(row)
    df = pd.DataFrame(all_meal_data).fillna("")
    st.table(df)


def display_seasonal_information(profile):
    """
    Display seasonal information about food preferences.
    """
    st.subheader("🌦️ Seasonal Information")
    st.write("Here are useful information about seasonal food, for which you expressed preferences, **available this month**. You can expand each section to view more information about each food item.")
    
    seasonal_preferences = profile.get_seasonal_preferences()
    for seasonal_food in seasonal_preferences:
        with st.expander(f"🍽️ **{seasonal_food.capitalize()}**"):
            if seasonal_food in food_infos.keys():
                food_info = food_infos[seasonal_food]
                display_food_info(food_info)
            else:
                st.write("📋 No information available.")


def display_food_info(food_info):
    """
    Display detailed information about a specific food item.
    """
    st.write(f"#### 📋 Description\n{food_info.get('description', 'No description available.')}")
    table_data = {
        "Benefits": ", ".join(food_info.get("benefits", ["No benefits available."])),
        "How to Store": food_info.get("how_to_store", "No information available."),
        "How to Choose": food_info.get("how_to_choose", "No information available."),
    }
    df = pd.DataFrame([table_data])
    st.table(df)
    st.write(f"#### 📋 Nutritional Intake\n{food_info.get('nutritional_intake', 'No information available.')}")
    st.write(f"#### 📋 Tips\n {food_info.get('tips', 'No tips available.')}")


# Call the function to display user profile
with st.spinner('Loading your profile...'):
    time.sleep(1)
    display_user_profile()
