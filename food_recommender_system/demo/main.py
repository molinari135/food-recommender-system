import streamlit as st

st.set_page_config(
    page_title="Food RecSys",  # Change tab title
    page_icon="🍽️",  # Change favicon (can be an emoji or URL to an image)
)

with st.sidebar:
    st.page_link('pages/1_home.py', label='Create or Load User Profile')
    st.page_link('pages/2_user_profile.py', label='User Profile Information')
    st.page_link('pages/3_meal_selection.py', label='Meal Selection')


# import streamlit as st
# from food_recommender_system.profiler import UserProfiler
# from pathlib import Path
# import pandas as pd
# import os
# import requests
# import json
# import time
# from datetime import datetime

# # Ensure the PROCESSED_DATA_PATH exists or use the default path
# BASE_PATH = Path(os.path.join(os.getcwd(), 'data'))
# RAW_DATA_PATH = Path(os.path.join(BASE_PATH, 'raw'))
# PROCESSED_DATA_PATH = Path(os.path.join(BASE_PATH, 'processed'))

# EXCLUDED_CATEGORIES = ["Baby Foods", "Meals, Entrees, and Side Dishes", "Soups", "Spices", "Greens"]

# food_dataset = pd.read_csv(RAW_DATA_PATH / "nutritional-facts.csv")
# food_dataset = food_dataset[~food_dataset['Category Name'].isin(EXCLUDED_CATEGORIES)]
# food_seasonality = json.load(open(RAW_DATA_PATH / "food-seasonality.json", "r"))


# # Function to load all available profiles (filenames)
# def load_profiles():
#     profiles = []
#     for filename in os.listdir(PROCESSED_DATA_PATH):
#         if filename.endswith(".json"):
#             profiles.append(filename)
#     return profiles


# # Get seasonal foods for the current month
# def get_seasonal_foods():
#     current_month = datetime.now().strftime("%m")  # e.g., "02" for February
#     seasonal_data = food_seasonality
#     country_data = seasonal_data.get("Italy")  # Adjust for your region if necessary
#     seasonal_foods = country_data.get(current_month, [])
#     return seasonal_foods


# def categorize_foods():
#     seasonal_foods = get_seasonal_foods()

#     seasonal = []
#     non_seasonal = []

#     # Categorize foods
#     for _, row in food_dataset.iterrows():
#         food_name = row['Food Name']
#         if food_name in seasonal_foods:
#             seasonal.append(food_name)
#         else:
#             non_seasonal.append(food_name)

#     return seasonal, non_seasonal


# # Function to get the current meal time based on the system clock
# def get_current_meal_time():
#     current_hour = datetime.now().hour
    
#     if 6 <= current_hour < 10:
#         return "Breakfast"
#     elif 11 <= current_hour < 15:
#         return "Lunch"
#     elif 16 <= current_hour < 20:
#         return "Dinner"
#     else:
#         return "Snack"  # For times outside typical meal times


# def load_user_profile():
#     profiles = load_profiles()

#     # Ensure session state for selected profile
#     if "selected_profile" not in st.session_state:
#         st.session_state.selected_profile = "-- Create a new profile --"

#     # Sidebar for selecting a profile
#     selected_profile = st.sidebar.selectbox(
#         "Select an existing profile",
#         ["-- Create a new profile --"] + profiles
#     )

#     # Function to display the current meal
#     def display_current_meal():
#         current_meal_time = get_current_meal_time()
#         current_day = datetime.now().weekday()  # Get today's weekday (e.g., 0 = Monday, 6 = Sunday)

#         # Load the user's profile and meals (you may want to fetch this from the session or database)
#         profile = UserProfiler.load_profile(PROCESSED_DATA_PATH / selected_profile)
#         st.subheader(f"Current {current_meal_time} for today:")

#         meals = profile.get_meals()
        
#         # Assuming that meals[current_meal_time] is a list where each day is a sublist of meals
#         today_meal = meals[current_meal_time][current_day]

#         if len(today_meal) == 3:
#             meal, alternative, choice = today_meal
#             st.markdown(f"🍽️ **Meal:** {', '.join(meal)}")
#             st.markdown(f"  🔄 **Alternative:** {', '.join(alternative)}")
#             st.markdown(f"  ✅ **User's choice:** {', '.join(choice)}")

#         elif len(today_meal) == 2:
#             # Ask the user to choose food-per-food and show justification for each choice
#             new_meal = []
#             for m, alt in zip(today_meal[0], today_meal[1]):  # Iterate through both meal and alternative lists
#                 # Display the food options for the user to select
#                 choice = st.radio(f"Choose between {m} and {alt}", options=[m, alt])

#                 # Get justification for the current choice
#                 justification = get_food_justification(m, alt)[0]

#                 st.markdown(justification['comparison'])
#                 st.markdown(justification['persuasion'])
#                 st.markdown("---")

#                 # Add the choice to the new meal list
#                 new_meal.append(choice)

#             # Once the user has made their choices, append the new meal to meals
#             if st.button("Confirm meal"):
#                 # Create a new meal, assuming this is the final choice
#                 updated_meal = (new_meal, today_meal[1], new_meal)
#                 meals[current_meal_time][current_day] = updated_meal  # Update the meal for today

#                 # Update the profile with the new meal
#                 profile.set_meals(meals)

#                 # Save the profile again
#                 profile.save_profile(PROCESSED_DATA_PATH / selected_profile)

#                 st.success("Meal updated successfully!")
#                 st.write(f"Your updated meal is: {', '.join(new_meal)}")

#         else:
#             st.warning(f"Unexpected meal structure: {today_meal}")

#     # Function to call the /justify API and get the justification
#     def get_food_justification(meal_1: list, meal_2: list):
#         data = {
#             "meal_1": [meal_1],
#             "meal_2": [meal_2]
#         }

#         response = requests.post("http://127.0.0.1:8000/justify", json=data)

#         if response.status_code == 200:
#             justification_data = response.json()
#             return justification_data["justification"]


#     # If the user selects a profile, load it
#     if selected_profile != "-- Create a new profile --":
#         st.session_state.selected_profile = selected_profile  # Update session state
#         profile = UserProfiler.load_profile(PROCESSED_DATA_PATH / selected_profile)

#         # Sidebar button to display the current meal
#         show_meal_button = st.sidebar.button("Show Current Meal")
        
#         if show_meal_button:
#             # When the button is clicked, show the current meal instead of the profile
#             display_current_meal()

#         else:
#             # Display the profile if the button has not been clicked
#             st.title(f"👤 Profile: {selected_profile}")

#             # Display Intolerances
#             st.subheader("🚫 Intolerances")
#             intolerances = profile.get_intolerances()
#             st.write(", ".join(intolerances[0]) if intolerances else "No intolerances listed.")

#             # Display Food Preferences
#             st.subheader("🍽️ Food Preferences")
#             food_preferences = profile.get_food_preferences()
#             st.write(", ".join(food_preferences) if food_preferences else "No food preferences listed.")

#             # Display Seasonal Preferences
#             st.subheader("🌱 Seasonal Preferences")
#             seasonal_preferences = profile.get_seasonal_preferences()
#             st.write(", ".join(seasonal_preferences) if seasonal_preferences else "No seasonal preferences listed.")

#             # Display Meals with Collapsible Sections
#             st.subheader("🥗 Meals")
#             meals = profile.get_meals()
#             if meals:
#                 for meal_time, meals_list in meals.items():
#                     with st.expander(f"**{meal_time.capitalize()}** ({len(meals_list)} options)"):

#                         for meal_item in meals_list:
#                             # If the item has 3 values, unpack it as meal, alternative, and choice
#                             if len(meal_item) == 3:
#                                 meal, alternative, choice = meal_item
#                                 st.markdown(f"🍽️ **Meal:** {', '.join(meal)}")
#                                 st.markdown(f"  🔄 **Alternative:** {', '.join(alternative)}")
#                                 st.markdown(f"  ✅ **User's choice:** {', '.join(choice)}")
#                             # If the item has only 2 values, unpack it as meal and alternative
#                             elif len(meal_item) == 2:
#                                 meal, alternative = meal_item
#                                 st.markdown(f"🍽️ **Meal:** {', '.join(meal)}")
#                                 st.markdown(f"  🔄 **Alternative:** {', '.join(alternative)}")
#                             else:
#                                 # Handle unexpected structure, if necessary
#                                 st.warning(f"Unexpected meal structure: {meal_item}")
#             else:
#                 st.write("No meals available.")

#             # Display Used Jolly
#             st.subheader("🎲 Used Jolly")
#             st.write("✅ Yes" if profile.used_jolly else "❌ No")

#     else:
#         # Create a new profile
#         st.subheader("Create a new profile")
#         new_profile = UserProfiler()
#         df = food_dataset.copy()

#         name = st.text_input("Enter your name:")
#         lactose_intolerance = st.selectbox("Do you have lactose intolerance?", options=["Yes", "No"])

#         if lactose_intolerance == "Yes":
#             df = df[~df['Category Name'].isin(['Dairy', 'Lactose-Free Dairy'])]

#         seasonal_foods, _ = categorize_foods()

#         # Dictionary to hold user selections for each category
#         user_preferences = {}
#         categories = df["Category Name"].unique().tolist()
#         category_foods = {category: df[df["Category Name"] == category]["Food Name"].tolist() for category in categories}

#         # For each category, ask the user to select foods
#         for category, foods in category_foods.items():
#             # Pre-fill multiselect with all foods by default
#             selected_foods = st.multiselect(
#                 f"Select your preferred {category} (remove the ones you don't like)",
#                 options=foods,
#                 default=foods  # Pre-selected by default
#             )

#             # Ensure at least one food remains selected
#             if not selected_foods:
#                 st.warning(f"You must select at least one food in {category}. Defaulting to the first item.")
#                 selected_foods = [foods[0]]  # Restore at least one default food

#             user_preferences[category] = selected_foods

#         # Now, categorize the selected foods into seasonal and non-seasonal
#         seasonal_preferences = []
#         non_seasonal_preferences = []

#         for category, selected_foods in user_preferences.items():
#             for food in selected_foods:
#                 if food in seasonal_foods:
#                     seasonal_preferences.append(food)
#                 elif category not in ["Fruits", "Vegetables"]:  # Exclude Fruits and Vegetables
#                     non_seasonal_preferences.append(food)

#         # Create and save the new profile
#         if st.button("Create Profile"):
#             new_profile.set_intolerances(["Lactose"] if lactose_intolerance == "Yes" else [])
#             new_profile.set_food_preferences(non_seasonal_preferences)
#             new_profile.set_seasonal_preferences(seasonal_preferences)
#             new_profile.set_used_jolly(False)

#             user_data = {
#                 "food_preferences": new_profile.get_food_preferences(),
#                 "seasonal_preferences": new_profile.get_seasonal_preferences(),
#                 "intolerances": new_profile.get_intolerances()
#             }

#             try:
#                 response = requests.post("http://127.0.0.1:8000/generate", json=user_data)
#                 response.raise_for_status()  # Raise an error for bad responses
#                 meals = response.json()["meals"]
#             except requests.exceptions.RequestException as e:
#                 st.error(f"Error generating meals: {e}")

#             new_profile.set_meals(meals)

#             filename = f"{name.replace(' ', '_').lower()}.json"
#             new_profile.save_profile(PROCESSED_DATA_PATH / filename)

#             # ✅ Set the new profile in session state
#             st.session_state.selected_profile = filename

#             st.success(f"Profile '{filename}' created successfully!")
#             time.sleep(1)  # Short delay for better UX

#             # ✅ Force rerun with the new profile selected
#             st.rerun()


# # Display the profile selection or creation interface
# load_user_profile()
