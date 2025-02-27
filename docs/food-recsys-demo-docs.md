# Food RecSys Demo Documentation

Welcome to the Food RecSys demo documentation! This guide will help you understand the structure and functionality of the Food RecSys demo application. The application is built using Streamlit and provides personalized food recommendations based on user profiles.

## Table of Contents
## Table of Contents

1. [Introduction](#introduction)
2. [File Structure](#file-structure)
3. [Main Components](#main-components)
    - [Home Page](#home-page)
    - [User Profile Page](#user-profile-page)
    - [Meal Selection Page](#meal-selection-page)
4. [How to Run the Application](#how-to-run-the-application)
5. [Conclusion](#conclusion)
6. [Contributors](#contributors)

## Introduction
Food RecSys is a personalized food recommendation system that helps users create and manage their food profiles, receive meal suggestions, and track their dietary preferences. The application is designed to be user-friendly and provides a seamless experience for managing food preferences and meal plans.

## File Structure
The application consists of the following main files:

- `main.py`: The main entry point of the application.
- `pages/1_home.py`: The home page where users can create or load their profiles.
- `pages/2_user_profile.py`: The user profile page displaying profile information.
- `pages/3_meal_selection.py`: The meal selection page for choosing meals based on recommendations.

## Main Components

### Home Page
**File:** `pages/1_home.py`

The home page allows users to create or load their profiles. Key functionalities include:
- Setting up the page configuration.
- Displaying sidebar navigation links.
- Loading or creating user profiles.
- Handling user preferences and intolerances.
- Saving new profiles.

### User Profile Page
**File:** `pages/2_user_profile.py`

The user profile page displays detailed information about the user's profile. Key functionalities include:
- Displaying additional information such as intolerances and jolly meal usage.
- Showing the meal plan for the week.
- Providing seasonal information about food preferences.
- Displaying detailed information about specific food items.

### Meal Selection Page
**File:** `pages/3_meal_selection.py`

The meal selection page allows users to choose meals based on recommendations. Key functionalities include:
- Displaying meal options for the current meal time.
- Allowing users to select between original and alternative meal options.
- Updating meal selections based on user choices.
- Providing a button for selecting a cheat meal if the user is feeling stressed.

### Main Application
**File:** `main.py`

The main application file sets up the overall structure and configuration of the application. Key functionalities include:
- Setting up the sidebar navigation.
- Loading paths and datasets.
- Loading and saving metrics.
- Providing introductory information and performance metrics.

## How to Run the Application
To run the Food RecSys demo application, follow these steps:

1. Ensure you have Python and Streamlit installed on your system.
2. Navigate to the project directory.
3. Run the following command to start the Streamlit application:
   ```bash
   streamlit run food_recommender_system/demo/main.py
   ```
4. Open the provided URL in your web browser to access the application.

## Conclusion
This documentation provides an overview of the Food RecSys demo application, including its file structure and main components. By following the instructions, you can easily run the application and explore its features. Enjoy your personalized food recommendations!

## Contributors
This demo was designed and implemented by **Ester Molinari** (@molinari135), MSc student in Computer Science @ University of Bari Aldo Moro during AY 2024/2025.