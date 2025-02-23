import streamlit as st
from food_recommender_system.profiler import UserProfiler
import food_recommender_system.demo.main as main
from datetime import datetime
from pathlib import Path
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Food RecSys - Meals",
    page_icon="🍽️",
)

# Constants
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
food_servings = st.session_state.food_servings


def display_meal_selection():
    """
    Main function for displaying meal selection.
    """
    if st.session_state.selected_profile == "-- Create a new profile --" or st.session_state.selected_profile is None:
        st.warning("⚠️ No user profile selected. Please create or load a user profile.")
        return

    selected_profile = st.session_state.selected_profile
    profile = UserProfiler.load_profile(Path(selected_profile))

    current_meal_time = main.get_current_meal_time()
    current_day = datetime.now().weekday()

    meals = profile.get_meals()
    today_meal = meals[current_meal_time][current_day]

    st.title(f"📅 Today's {current_meal_time}")

    if len(today_meal) == 3:
        display_three_meal_options(today_meal, profile, current_meal_time, current_day)
    elif len(today_meal) == 2:
        display_two_meal_options(today_meal, profile, current_meal_time, current_day)

    if current_meal_time in ["Lunch", "Dinner"] and not profile.used_jolly:
        display_stress_button(profile, current_meal_time, current_day)

    main.save_metrics()  # Save data to JSON


def display_three_meal_options(today_meal, profile, current_meal_time, current_day):
    """
    Display meal options when there are three variants: original, alternative, and choice.
    """
    meal, alternative, choice = today_meal

    with st.expander("ℹ️ How to read this table"):
        st.markdown("\n- The first row is the original meal\n- The second row is the alternative meal\n- The third row is your choice")

    all_meal_data = []

    for variant in [meal, alternative, choice]:
        row = {}
        for food_name in variant:
            category = food_dataset.loc[food_dataset["Food Name"] == food_name, "Category Name"]
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

    st.markdown("### ⭐ How satisfied were you with the recommendation?")
    sentiment_mapping = ["one", "two", "three", "four", "five"]
    selected = st.feedback("stars")

    if selected is not None:
        st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")
        st.session_state.persuasion_satisfaction.append(selected + 1)
        st.success("✅ Rating saved successfully!")


def display_two_meal_options(today_meal, profile, current_meal_time, current_day):
    """
    Display meal options when there are two variants: original and alternative.
    """
    st.markdown(f"""
            This is today's {current_meal_time.lower()}. If you are not satisfied with the generated meal, you can compose your own meal taking into account that:
            - The **first option** comes directly from your preferences\n
            - The **second option** is an alternative meal based on the same category of the first one, but with better nutritional values\n
            """)
    st.markdown("---")
    st.subheader("Choose and compose your meal")
    new_meal = []
    for m, alt in zip(today_meal[0], today_meal[1]):
        choice = st.radio(f"🍽️ Choose between {m} and {alt}", options=[m, alt])
        justification = main.get_food_justification(m, alt)
        if justification:
            with st.expander("ℹ️ Nutritional comparison"):
                st.markdown(justification[0]['comparison'])
            persuasion_text = justification[0]['persuasion']
            sentences = persuasion_text.split('\n')
            for sent in sentences:
                st.markdown(sent)
        new_meal.append(choice)
        st.markdown("---")

    if st.button("✅ Confirm meal"):
        update_meal_selection(profile, today_meal, new_meal, current_meal_time, current_day)


def update_meal_selection(profile, today_meal, new_meal, current_meal_time, current_day):
    """
    Update the meal selection based on user choices.
    """
    updated_meal = (today_meal[0], today_meal[1], new_meal)
    meals = profile.get_meals()
    meals[current_meal_time][current_day] = updated_meal
    profile.set_meals(meals)
    profile.save_profile(Path(st.session_state.selected_profile))

    for chosen_food, original_food, recommended_food in zip(new_meal, today_meal[0], today_meal[1]):
        if chosen_food == recommended_food:
            st.session_state.recsys_wins += 1  # Recommender won
            justification = main.get_food_justification(original_food, recommended_food)
            if justification:
                st.session_state.justification_success += 1  # Justification was persuasive
        else:
            st.session_state.user_wins += 1  # User rejected recommendation

        st.session_state.total_choices += 1  # Each food choice counts separately

    st.success("✅ Meal updated successfully!")
    st.rerun()


def display_stress_button(profile, current_meal_time, current_day):
    """
    Display a button for users to select a cheat meal if they are feeling stressed.
    """
    _, col2 = st.columns([8, 2])
    with col2:
        if st.button("😩 Are you feeling stressed?", help="Click if you had a bad day!"):
            user_fast_foods = main.get_user_fast_food_preferences(profile)

            if user_fast_foods:
                cheat_meal = main.get_cheat_meal(user_fast_foods)

                fast_food = cheat_meal["chosen_fast_food"] if cheat_meal else None
                fast_food_alt = cheat_meal["recommended_cheat_meal"][0] if cheat_meal else None

                if cheat_meal:
                    st.success(f"🍔 Cheat meal granted: {fast_food}")

                    profile.used_jolly = True

                    meals = profile.get_meals()
                    meals[current_meal_time][current_day] = (
                        [fast_food],
                        [fast_food_alt]
                    )

                    profile.set_meals(meals)
                    profile.save_profile(Path(st.session_state.selected_profile))

                    st.warning("⚠️ Your meal has been updated. Choose your preference below.")
                    st.rerun()
            else:
                st.warning("⚠️ No fast food preferences found in your selected foods.")


display_meal_selection()
