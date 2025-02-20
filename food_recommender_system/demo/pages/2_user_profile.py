import streamlit as st
from food_recommender_system.profiler import UserProfiler
from pathlib import Path
import pandas as pd
import json
import os


st.set_page_config(
    page_title="Food RecSys - User Profile",  # Change tab title
    page_icon="🍽️",  # Change favicon (can be an emoji or URL to an image)
)


BASE_PATH = Path(os.path.join(os.getcwd(), 'data'))
RAW_DATA_PATH = Path(os.path.join(BASE_PATH, 'raw'))


with st.sidebar:
    st.page_link('pages/1_home.py', label='Create or Load User Profile')
    st.page_link('pages/2_user_profile.py', label='User Profile Information')
    st.page_link('pages/3_meal_selection.py', label='Meal Selection')


food_dataset = pd.read_csv(RAW_DATA_PATH / "nutritional-facts.csv")
food_infos = json.load(open(RAW_DATA_PATH / "food-infos.json", "r"))


# Main function for displaying user profile
def display_user_profile():
    if st.session_state.selected_profile == "-- Create a new profile --" or "selected_profile" not in st.session_state:
        st.warning("No user profile selected. Please create or load a user profile.")
        return

    selected_profile = st.session_state.selected_profile
    profile = UserProfiler.load_profile(Path(selected_profile))

    profile_name = selected_profile[:-5].replace('_', ' ').capitalize()
    st.title(f"Welcome, {profile_name}!")

    # Display Intolerances
    st.subheader("🚫 Intolerances")
    intolerances = profile.get_intolerances()
    if intolerances and intolerances[0]:
        st.write(", ".join(intolerances[0]))
    else:
        st.write("No intolerances listed.")

    # # Display Food Preferences
    # st.subheader("🍽️ Food Preferences")
    # food_preferences = profile.get_food_preferences()
    # st.write(", ".join(food_preferences) if food_preferences else "No food preferences listed.")

    # # Display Seasonal Preferences
    # st.subheader("🌱 Seasonal Preferences")
    # seasonal_preferences = profile.get_seasonal_preferences()
    # st.write(", ".join(seasonal_preferences) if seasonal_preferences else "No seasonal preferences listed.")

    st.subheader("🥗 Meals")
    meals = profile.get_meals()

    if meals:
        for meal_time, meal_options in meals.items():
            with st.expander(f"**{meal_time.capitalize()}** ({len(meal_options)} days)"):
                # Loop over each day
                for day_index, meal_variants in enumerate(meal_options):
                    st.markdown(f"#### 📅 Day {day_index + 1}")  # Day Header
                    
                    all_meal_data = []

                    # Loop over meal variants (different options for that meal)
                    for variant in meal_variants:
                        row = {}

                        # Process each food item
                        for food_name in variant:
                            category = food_dataset.loc[
                                food_dataset["Food Name"] == food_name, "Category Name"
                            ]
                            category_name = category.values[0] if not category.empty else "Unknown"

                            # Store food under its category
                            row[category_name] = food_name  

                        all_meal_data.append(row)

                    # Convert list to DataFrame
                    df = pd.DataFrame(all_meal_data).fillna("")  # Fill empty values for display

                    # Display the table
                    st.table(df)
    else:
        st.write("No meals available.")

    st.subheader("🌦️ Seasonal Information")
    seasonal_preferences = profile.get_seasonal_preferences()

    for seasonal_food in seasonal_preferences:
        with st.expander(f"🍽️ **{seasonal_food.capitalize()}**"):
            if seasonal_food in food_infos.keys():
                food_info = food_infos[seasonal_food]

                # Display general information
                st.write(f"#### Description\n{food_info.get('description', 'No description available.')}")
                
                # Prepare table data
                table_data = {
                    "Benefits": ", ".join(food_info.get("benefits", ["No benefits available."])),
                    "How to Store": food_info.get("how_to_store", "No information available."),
                    "How to Choose": food_info.get("how_to_choose", "No information available."),
                }

                # Convert to DataFrame for display
                df = pd.DataFrame([table_data])

                # Display table
                st.table(df)
                st.write(f"#### Nutritional Intake\n{food_info.get('nutritional_intake', 'No information available.')}")
                st.write(f"#### Tips\n {food_info.get('tips', 'No tips available.')}")

            else:
                st.write("No information available.")


# Call the function to display user profile
display_user_profile()
