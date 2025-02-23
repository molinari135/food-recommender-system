import streamlit as st
from pathlib import Path
import pandas as pd
from datetime import datetime
import requests
import json
import os

# Set the page config
st.set_page_config(
    page_title="Food RecSys",
    page_icon="🍽️",
)


# Sidebar navigation
def setup_sidebar():
    with st.sidebar:
        st.page_link('main.py', label='🏠 Home')
        st.page_link('pages/1_home.py', label='👤 Create or Load User Profile')
        st.page_link('pages/2_user_profile.py', label='📋 User Profile Information')
        st.page_link('pages/3_meal_selection.py', label='🍽️ Meal Selection')


# Paths and dataset setup
def setup_paths_and_data():
    BASE_PATH = Path(os.path.join(os.getcwd(), 'data'))
    RAW_DATA_PATH = Path(os.path.join(BASE_PATH, 'raw'))
    PROCESSED_DATA_PATH = Path(os.path.join(BASE_PATH, 'processed'))

    EXCLUDED_CATEGORIES = ["Baby Foods", "Meals, Entrees, and Side Dishes", "Soups", "Spices", "Greens"]

    food_dataset = pd.read_csv(RAW_DATA_PATH / "nutritional-facts.csv")
    food_dataset = food_dataset[~food_dataset['Category Name'].isin(EXCLUDED_CATEGORIES)]

    food_seasonality = json.load(open(RAW_DATA_PATH / "food-seasonality.json", "r"))
    food_servings = json.load(open(RAW_DATA_PATH / "food-servings.json", "r"))
    food_infos = json.load(open(RAW_DATA_PATH / "food-infos.json", "r"))

    st.session_state.update({
        "BASE_PATH": BASE_PATH,
        "RAW_DATA_PATH": RAW_DATA_PATH,
        "PROCESSED_DATA_PATH": PROCESSED_DATA_PATH,
        "EXCLUDED_CATEGORIES": EXCLUDED_CATEGORIES,
        "food_dataset": food_dataset,
        "food_seasonality": food_seasonality,
        "food_servings": food_servings,
        "food_infos": food_infos
    })


def load_metrics():
    """Load metrics from the metrics file into session state."""
    METRICS_FILE = Path("metrics.json")
    if METRICS_FILE.exists():
        with open(METRICS_FILE, "r") as f:
            data = json.load(f)
        st.session_state.update({
            "recsys_wins": data.get("recsys_wins", 0),
            "user_wins": data.get("user_wins", 0),
            "justification_success": data.get("justification_success", 0),
            "total_choices": data.get("total_choices", 0),
            "persuasion_satisfaction": data.get("persuasion_satisfaction", [])
        })
    else:
        st.session_state.update({
            "recsys_wins": 0,
            "user_wins": 0,
            "justification_success": 0,
            "total_choices": 0,
            "persuasion_satisfaction": []
        })


def save_metrics():
    """Save metrics from session state to the metrics file."""
    METRICS_FILE = Path("metrics.json")
    data = {
        "recsys_wins": st.session_state.recsys_wins,
        "user_wins": st.session_state.user_wins,
        "justification_success": st.session_state.justification_success,
        "total_choices": st.session_state.total_choices,
        "persuasion_satisfaction": st.session_state.persuasion_satisfaction,
    }
    with open(METRICS_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_profiles():
    """Load user profiles from the processed data path."""
    profiles = []
    for filename in os.listdir(st.session_state.PROCESSED_DATA_PATH):
        if filename.endswith(".json"):
            profiles.append(filename)
    return profiles


def categorize_foods():
    """Categorize foods into seasonal and non-seasonal."""
    seasonal_foods = get_seasonal_foods()
    seasonal = []
    non_seasonal = []

    for _, row in st.session_state.food_dataset.iterrows():
        food_name = row['Food Name']
        if food_name in seasonal_foods:
            seasonal.append(food_name)
        else:
            non_seasonal.append(food_name)

    return seasonal, non_seasonal


def get_seasonal_foods():
    """Get the list of seasonal foods for the current month."""
    current_month = datetime.now().strftime("%m")
    seasonal_data = st.session_state.food_seasonality
    country_data = seasonal_data.get("Italy")  # Adjust for different region if necessary
    seasonal_foods = country_data.get(current_month, [])
    return seasonal_foods


def get_current_meal_time():
    """Get the current meal time based on the hour of the day."""
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
    """Get a cheat meal suggestion based on fast food preferences."""
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


def get_food_justification(meal_1, meal_2):
    """Get justification for choosing between two meals."""
    data = {"meal_1": [meal_1], "meal_2": [meal_2]}
    response = requests.post("https://molinari135-food-recsys-api.hf.space/justify", json=data)
    if response.status_code == 200:
        return response.json()["justification"]


def get_user_fast_food_preferences(profile):
    """Get the user's fast food preferences from their profile."""
    user_preferences = profile.get_food_preferences()
    fast_foods = []

    for food in user_preferences:
        category = st.session_state.food_dataset.loc[st.session_state.food_dataset["Food Name"] == food, "Category Name"]
        if not category.empty and category.values[0] == "Fast Foods":
            fast_foods.append(food)

    return fast_foods


# Main execution
setup_sidebar()
setup_paths_and_data()
load_metrics()
st.session_state.selected_profile = None

# Title and introduction
st.title("🍴 Welcome to Food RecSys!")
st.markdown("> 🍽️ Your personalized food recommendation system!")
st.markdown("---")

st.markdown("### 📊 Recommender Performances")

if st.session_state.total_choices > 0:
    win_rate = (st.session_state.recsys_wins / st.session_state.total_choices) * 100
    rejection_rate = (st.session_state.user_wins / st.session_state.total_choices) * 100
    avg_persuasion = (sum(st.session_state.persuasion_satisfaction) / len(st.session_state.persuasion_satisfaction))

    col1, col2, col3 = st.columns(3)
    col1.metric(label="🏆 Win Rate", value=f"{win_rate:.2f}%")
    col2.metric(label="❌ Rejection Rate", value=f"{rejection_rate:.2f}%")
    col3.metric(label="⭐ Avg. Persuasion Rating", value=f"{avg_persuasion:.2f}")
else:
    st.info("No choices made yet.")

with st.expander("📈 What do these values mean?"):
    st.markdown("""
    These values help us understand how well the recommender system is performing:
    - **Win Rate**: Percentage of times the recommender system's suggestion was chosen.
    - **Rejection Rate**: Percentage of times the user rejected the recommender system's suggestion.
    - **Avg. Persuasion Rating**: Average rating given by the user for the persuasion message of the recommendation.
    """)

# Introduction with expandable sections
with st.expander("📖 How Food RecSys Works"):
    st.markdown("""
    ### 👤 **Create Your Profile**
    - Enter your name and dietary preferences.
    - Load an existing profile or create a new one.

    ### 🍲 **Get Personalized Meal Suggestions**
    - Receive tailored meal suggestions for **Breakfast, Lunch, and Dinner**.
    - Compare meal alternatives with explanations.

    ### 🍔 **Have a Cheat Meal!**
    - Feeling stressed? Get a fast food suggestion once a week.

    ### 🛠️ **How to Navigate:**
    - **Create or Load Profile**: Start by setting up your preferences.
    - **User Profile**: View and update your profile.
    - **Meal Selection**: Choose meals based on recommendations.

    🚀 **Start now and improve your eating habits!**
    """)

with st.expander("🤔 Why Choose Food RecSys?"):
    st.markdown("""
    Food RecSys simplifies meal planning while ensuring a **healthy and tasty** experience:
    - 🌱 Seasonal meal suggestions.
    - 🥗 Personalized recommendations.
    - 🍔 Occasional indulgences!

    No more meal indecision—let's make food fun! 🍲✨
    """)

st.markdown("---")

# Call-to-Action Button
st.markdown("### Ready to Get Started?")
if st.button("👤 Create or Load Your Profile"):
    st.switch_page("pages/1_home.py")
