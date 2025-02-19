import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Food Recommender System API Demo")

# Test Recommender Endpoint
st.header("Get Food Recommendation")

food_name = st.text_input("Enter a food name:")
category = st.text_input("Enter a category (optional):")
low_density = st.checkbox("Prefer low energy density?", True)

if st.button("Get Recommendation"):
    payload = {
        "food_name": food_name,
        "category": category or None,
        "low_density": low_density
    }
    response = requests.post(f"{API_URL}/recommend", json=payload)

    if response.status_code == 200:
        st.write("Recommended foods:")
        st.json(response.json())
    else:
        st.error("Error: " + response.text)


# Test Meal Generation Endpoint
st.header("Generate Weekly Meals")

food_preferences = st.text_area("Enter preferred foods (comma-separated)").split(", ")
seasonal_preferences = st.text_area("Enter seasonal preferences (comma-separated)").split(", ")
intolerances = st.text_area("Enter intolerances (comma-separated)").split(", ")

if st.button("Generate Weekly Meals"):
    payload = {
        "food_preferences": food_preferences,
        "seasonal_preferences": seasonal_preferences,
        "intolerances": intolerances if intolerances != [''] else []
    }
    response = requests.post(f"{API_URL}/generate", json=payload)

    if response.status_code == 200:
        st.write("Generated weekly meal plan:")
        st.json(response.json())
    else:
        st.error("Error: " + response.text)


# Test Justification Endpoint
st.header("Compare Two Meals")

meal_1 = st.text_area("Enter Meal 1 (comma-separated)").split(",")
meal_2 = st.text_area("Enter Meal 2 (comma-separated)").split(",")

if st.button("Get Justification"):
    payload = {
        "meal_1": meal_1,
        "meal_2": meal_2
    }
    response = requests.post(f"{API_URL}/justify", json=payload)

    if response.status_code == 200:
        st.write("Justification:")
        st.json(response.json())
    else:
        st.error("Error: " + response.text)
