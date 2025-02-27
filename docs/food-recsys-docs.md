# Food Recommender System Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Datasets](#datasets)
    1. [food-infos.json](#food-infosjson)
    2. [food-servings.json](#food-servingsjson)
    3. [food-seasonality.json](#food-seasonalityjson)
    4. [nutritional-facts.csv](#nutritional-factscsv)
3. [Configuration File](#configuration-file)
4. [Data Loader](#data-loader)
5. [Main](#main)
6. [Justificator](#justificator)
7. [Meal Generator](#meal-generator)
8. [Mood Modifier](#mood-modifier)
9. [User Profiler](#user-profiler)
10. [Recommender](#recommender)
11. [Contributors](#contributors)

## Introduction
The Food Recommender System is designed to help users create personalized meal plans based on their preferences, intolerances, and seasonal food availability. This documentation provides an overview of the system's components and their functionalities.

![foodrecsys](https://github.com/user-attachments/assets/0040e027-d13c-4145-a19d-3ca0138ce57d)

## Datasets

The Food Recommender System utilizes several datasets to provide accurate and personalized meal recommendations. Below is an overview of the key files used:

### food-infos.json
**Filepath:** `food-recommender-system/data/raw/food-infos.json`

This JSON file contains detailed information about various foods, including storage tips and other useful advice. Each entry provides practical tips on how to store and consume different types of fruits.

These information have been manually scraped from [Altroconsumo's Fruit and Vegetable Calendar](https://www.altroconsumo.it/alimentazione/fare-la-spesa/consigli/calendario-frutta-verdura).

### food-servings.json
**Filepath:** `food-recommender-system/data/raw/food-servings.json`

This JSON file outlines the recommended serving sizes and weekly consumption frequencies for different food categories. It includes tips on how to measure servings and provides guidelines for a balanced diet.

These information have been manually scraped from [LARN Standard Serving Sizes](https://sinu.it/wp-content/uploads/2019/07/20141111_LARN_Porzioni.pdf).

### food-seasonality.json
**Filepath:** `food-recommender-system/data/raw/food-seasonality.json`

This JSON file lists the seasonal availability of various fruits and vegetables in Italy. It helps the system recommend foods that are in season, ensuring freshness and better nutritional value.

These information have been manually scraped from [Altroconsumo's Fruit and Vegetable Calendar](https://www.altroconsumo.it/alimentazione/fare-la-spesa/consigli/calendario-frutta-verdura).

### nutritional-facts.csv
**Filepath:** `food-recommender-system/data/raw/nutritional-facts.csv`

This CSV file contains comprehensive nutritional information for a wide range of foods. The dataset has been heavily modified from its original version on Kaggle to better fit the needs of the Food Recommender System. It includes data on calories, macronutrients, vitamins, and minerals for each food item.

For more details on the original dataset, you can visit the [Kaggle page](https://www.kaggle.com/datasets/beridzeg45/food-nutritional-facts).

These files collectively provide the necessary data to generate personalized and nutritionally balanced meal plans for users.

## Configuration file
**Filepath:** `food-recommender-system/food_recommender_system/config.py`

The `config.py` file contains configuration settings and constants used throughout the system.

### Key Components:
- **Paths:** Defines the base paths for raw and processed data.
- **Macronutrients:** List of macronutrients considered in the system.
- **Excluded Categories:** Categories of food to be excluded from recommendations.
- **Intolerances:** Lists of food categories for lactose and gluten intolerance.
- **Meal Generation Categories:** Categories of food considered for meal generation.
- **Preferences:** Default food preferences for users with and without intolerances.

## Data Loader
**Filepath:** `food-recommender-system/food_recommender_system/dataloader.py`

The `dataloader.py` file contains the `DataLoader` class, which handles loading and preprocessing data for the recommender system.

### Key Methods:
- `load_csv(filename: Path)`: Loads a CSV file and returns a pandas DataFrame.
- `load_json(filename: Path)`: Loads a JSON file and returns its content as a dictionary.
- `filter_categories(df: pd.DataFrame, exclude_categories: list)`: Filters out rows with specific category names.
- `fill_missing_values(df: pd.DataFrame, fill_value: int)`: Replaces NaN values with a specified fill value.
- `get_nutritional_info(df: pd.DataFrame, food_name: str, only_numbers: bool)`: Retrieves nutritional information for a specific food item.
- `compute_energy_density(df: pd.DataFrame, food_name: str)`: Computes the energy density of a given food item.
- `get_food_category(df: pd.DataFrame, food_name: str)`: Retrieves the category of a specific food item.

## Main
**Filepath:** `food-recommender-system/food_recommender_system/main.py`

The `main.py` file contains the main entry point for the Food Recommender System CLI.

### Key Functions:
- `show_menu()`: Displays the main menu.
- `create_or_load_user()`: Creates or loads a user profile.
- `display_current_meal_and_alternatives(user: UserProfiler, filename: Path)`: Displays the current meal and its alternatives.
- `display_weekly_meal_plan(user: UserProfiler)`: Displays the weekly meal plan.
- `learn_about_seasonal_food(food_info: dict)`: Provides information about seasonal foods.
- `main()`: The main function that runs the CLI.

## Justificator
**Filepath:** `food-recommender-system/food_recommender_system/justificator.py`

The `justificator.py` file contains functions to justify and explain meal recommendations.

### Key Functions:
- `print_meal(meal: list, df: pd.DataFrame, servings: dict)`: Prints the details of a meal.
- `print_full_week_meals(user: UserProfiler, df: pd.DataFrame, servings: dict)`: Prints the full week's meal plan.
- `compare_meals(df: pd.DataFrame, meal1: list, meal2: list, verbose: bool)`: Compares two meals and provides a detailed comparison.
- `recommend_seasonal(seasonal_info: dict, food_name: str)`: Provides recommendations for seasonal foods.
- `get_current_meal(user: UserProfiler, meal_name: str, debug: bool)`: Retrieves the current meal for the user.
- `choose_foods_in_current_meal(user: UserProfiler, filename: Path, df: pd.DataFrame)`: Allows the user to choose foods in the current meal.

## Meal Generator
**Filepath:** `food-recommender-system/food_recommender_system/mealgen.py`

The `mealgen.py` file contains functions to generate meals based on user preferences and nutritional information.

### Key Functions:
- `generate_meal(preferences_df: pd.DataFrame, filtered_df: pd.DataFrame, category: str)`: Generates a meal based on user preferences.
- `generate_breakfast(preferences_df: pd.DataFrame, filtered_df: pd.DataFrame)`: Generates a breakfast meal.
- `generate_snack(preferences_df: pd.DataFrame, filtered_df: pd.DataFrame)`: Generates a snack.
- `compute_meal_calories(meal: list, df: pd.DataFrame, servings: pd.DataFrame, verbose: bool)`: Computes the total calories for a given meal.
- `generate_weekly_meal_plan(df: pd.DataFrame, servings: dict, user_profiler: UserProfiler, filename: Path)`: Generates a weekly meal plan.

## Mood Modifier
**Filepath:** `food-recommender-system/food_recommender_system/moodmod.py`

The `moodmod.py` file contains functions to modify meals based on the user's mood.

### Key Functions:
- `change_meal(user: UserProfiler, df: pd.DataFrame, meal_name: str, filename: Path)`: Suggests a new meal based on user mood and preferences.
- `reset_jolly_if_new_week(user: UserProfiler)`: Resets the jolly flag if today is the first day of the week.

## User Profiler
**Filepath:** `food-recommender-system/food_recommender_system/profiler.py`

The `profiler.py` file contains the `UserProfiler` class, which manages user profiles.

### Key Methods:
- `set_intolerances(intolerance: str)`: Adds an intolerance to the profile.
- `get_intolerances() -> list`: Retrieves the user's intolerances.
- `set_food_preferences(food_list: list)`: Updates food preferences.
- `get_food_preferences() -> list`: Retrieves the user's food preferences.
- `set_seasonal_preferences(food_list: list)`: Updates seasonal preferences.
- `get_seasonal_preferences() -> list`: Retrieves the user's seasonal preferences.
- `set_meals(meals: dict)`: Updates the user's meals.
- `get_meals() -> dict`: Retrieves the user's meals.
- `set_used_jolly(value: bool)`: Sets the used jolly flag.
- `get_used_jolly() -> bool`: Retrieves the used jolly flag.
- `save_profile(filename: Path)`: Saves the user profile to a file.
- `check_profile(filename: Path)`: Checks if a profile exists and creates a new one if it doesn't.
- `load_profile(filename: Path)`: Loads a user profile from a file.
- `create_new_profile(filename: Path)`: Creates a new user profile.

## Recommender
**Filepath:** `food-recommender-system/food_recommender_system/recommender.py`

The `recommender.py` file contains functions to recommend foods based on user preferences and nutritional information.

### Key Functions:
- `get_seasonal_food(df: pd.DataFrame, seasonality: dict, nationality: str)`: Gets the seasonal fruits and vegetables for a given nationality.
- `get_similar_food(df: pd.DataFrame, food_name: str, same_category: bool, low_density_food: bool)`: Gets a list of foods similar to the given food.
- `ask_user_preferences(df: pd.DataFrame, user_profiler: UserProfiler, filename: Path)`: Asks the user for their food preferences and saves them to a profile.
- `ask_seasonal_preferences(df: pd.DataFrame, seasonality: dict, user_profiler: UserProfiler, filename: Path, info_file: dict)`: Asks the user for their seasonal food preferences and saves them to a profile.

## Contributors
This system was designed and implemented by **Ester Molinari** (@molinari135), MSc student in Computer Science @ University of Bari Aldo Moro during AY 2024/2025.