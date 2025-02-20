import streamlit as st

# Set the page config
st.set_page_config(
    page_title="Food RecSys",  # Change tab title
    page_icon="🍽️",  # Change favicon (can be an emoji or URL to an image)
)

# Sidebar navigation
with st.sidebar:
    st.page_link('main.py', label='🏠 Home')
    st.page_link('pages/1_home.py', label='👤 Create or Load User Profile')
    st.page_link('pages/2_user_profile.py', label='📋 User Profile Information')
    st.page_link('pages/3_meal_selection.py', label='🍽️ Meal Selection')

st.session_state.selected_profile = None

# Main content
st.title("🍴 Welcome to Food RecSys!")

# Introduction Text
st.markdown("""
🍽️ Welcome to **Food RecSys**, your personalized food recommendation system!
With Food RecSys, we help you choose balanced meals tailored to your preferences and dietary needs. Here's how the app works:

### 1. 👤 **Create Your Profile**
To get started, you'll need to create your profile. This includes:
- **Your Name**: Just a simple way to personalize the experience.
- **Dietary Preferences**: Do you have any food intolerances (e.g., lactose intolerance)? We can adjust the meal suggestions accordingly.

You can either **load an existing profile** or create a new one from scratch.

### 2. 🍲 **Get Personalized Meal Suggestions**
Once your profile is set, we will suggest meals for you based on your preferences. Each day, you'll receive:
- **Breakfast, Lunch, and Dinner** suggestions.
- You can choose between meal alternatives and learn about the benefits of each option.

### 3. 🍔 **Have a Cheat Meal!**
Feeling like a cheat meal? If you're having a rough day, you can use your **jolly** to swap your regular meal for a fast food alternative.

Click **“Are you feeling stressed?”** if you'd like to get a tasty fast food recommendation.

> This can only be done once a week, so choose wisely! 🍔🍟

### How to Navigate:
- **Create or Load Profile**: Begin by setting up your preferences.
- **User Profile**: See and update your profile details.
- **Meal Selection**: View and choose meals based on your preferences.

🚀 Let's get started by creating your profile!
""")

# Button to navigate to profile creation
if st.button("Create or Load Profile"):
    st.switch_page("pages/1_home.py")

# Explanation about how the app works with visuals
st.markdown("""
### 🤔 Why Food RecSys?
Food RecSys is designed to make your daily meal planning simple and fun. Whether you are health-conscious or just want something quick and tasty, we’ve got you covered! You can:
- 🌱 Explore meal suggestions based on **seasonal** ingredients.
- 🥗 Get personalized alternatives that fit your dietary needs.
- 🍰 Indulge in a cheat meal when you deserve a treat.

🍲✨ No more wasting time deciding what to eat—Food RecSys is here to help you eat better every day.

🌱 Let's begin your food journey today!
""")
