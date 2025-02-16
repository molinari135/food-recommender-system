# Food Recommender System with Justification
> Food Recommender System with recipe and justification generation for Semantics in Intelligent Information Access and Recommender Systems @ Università degli Studi di Bari Aldo Moro, AY 2024/25

![Architecture overview](docs\recsysfloww.png)

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Overview
The Food Recommender System is designed to provide personalized recipe recommendations and generate justifications for the recommendations. This project is part of the Semantics in Intelligent Information Access course and Recommender System course at Università degli Studi di Bari Aldo Moro for the academic year 2024/25.

The system's architecture includes multiple components, each responsible for different aspects of meal recommendation and justification. Below is a breakdown of the system's key modules and functionalities:

- **User Profiling**: Captures and updates user preferences, intolerances, and meal history.
- **Meal Generation**: Creates meals based on user preferences, available ingredients, and nutritional data.
- **Justification**: Provides reasoning behind meal recommendations, including nutritional benefits.
- **Mood-based Meal Modification**: Suggests meals based on the user’s mood, e.g., recommending comfort foods if the user is stressed.
- **Seasonal Recommendations**: Encourages consumption of seasonal ingredients based on environmental and health benefits.

## Project Structure
The project is structured as follows:

```
food_recommender_system/
│
├── app.py
├── config.py
├── dataloader.py
├── justificator.py
├── main.py
├── mealgen.py
├── moodmod.py
├── profiler.py
└── recommender.py
```

- `app.py`: Main entry point for the Streamlit application.
- `config.py`: Configuration file containing paths for data files, preferences, and constants.
- `dataloader.py`: Handles loading and processing of nutritional and ingredient data.
- `justificator.py`: Provides meal justification and comparison, including nutritional analysis and seasonality suggestions.
- `main.py`: Main script that integrates all components of the system for generating and displaying recommendations.
- `mealgen.py`: Contains functions related to meal generation.
- `moodmod.py`: Handles mood-based meal suggestions and resets the "jolly" flag for the user.
- `profiler.py`: Manages user profiles and preferences.
- `recommender.py`: Core recommendation logic for suggesting meals and ingredients.

## Features

### 1. User Profiling and Preferences

- Collects and stores user data such as food preferences, intolerances (e.g., lactose or gluten), and dietary restrictions.
- Users can modify their preferences based on their dietary needs, nationality, and lifestyle.
- Profiles are stored in a JSON format for easy retrieval and modification.

### 2. Meal Generation

- Recommends meals based on user preferences and nutritional guidelines.
- The system suggests different meal types such as breakfast, lunch, dinner, and snacks.
- For each meal, a justification is provided based on the nutritional content and benefits of the chosen ingredients.

### 3. Nutritional Comparison

- Allows users to compare two meals or ingredients based on macronutrient content.
- Comparison includes calories, protein, carbohydrates, fats, fiber, and other macronutrients.
- The system provides a detailed comparison and suggests which meal/ingredient is a better choice based on the user's goals (e.g., weight loss, muscle gain).

### 4. Mood-based Meal Suggestions

- Suggests meals based on the user’s mood (e.g., stressed, tired).
- The system allows the user to “reset” their jolly meal for the week, offering comfort foods or special treats if the user is feeling stressed.
- The system prompts the user for input, like whether they are stressed, and responds with mood-appropriate meal recommendations.

### 5. Seasonal Recommendations

- Recommends meals based on seasonal ingredients.
- Suggests ingredients with lower environmental impact by promoting local and seasonal produce.
- Seasonal foods are encouraged for their higher nutritional content and better flavor.


## Installation
To install the Food Recommender System, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/molinari135/food-recommender-system.git
    ```
    
2. Navigate to the project directory:
    ```bash
    cd food-recommender-system
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
To use the Food Recommender System, run the following command:
```bash
python food_recommender_system/main.py
```

The system provides two standard profiles: `default` and `lactose`. You can also define a new username and it will be added automatically.
To start using the Food Recommender System, follow these steps:

```bash
🆔 Enter username to create or load your profile:
```

If you load `default`, the main menu will appear:

```bash
🍽️ Welcome to the Food Recommender System CLI! 🍽️
1️. Create or Load User
2️. Display Current Meal and Alternatives
3️. Display Weekly Meal Plan
4️. Learn About Seasonal Food
0️. Exit
Enter your choice (0-4): 
```

Follow the on-screen instructions to get personalized recipe recommendations.

> If you do not write any number during the preferences selection, the system will load default choices!

> If you do not write any number during the seasonal preference selection, the system will load every seasonal food!

### Create or Load User

This option allows to load a different user or create a new one, as in the beginning of the application.

### Display Current Meal and Alternatives

Using system's calendar and clock, this option will show the current meal of the day and, if needed, will ask the user to choose the actual meal by selecting a food for each section proposed. Then, it will be saved in the user's profile.

### Display Weekly Meal Plan

This option will show the entire generated weekly plan with breakfasts, snacks, lunches and dinners. The first meal shown is the one generated starting from user's preferences, then it will show an alternative version with a lower energy density (which is the standardized ratio between calories and weight). It will also display the actual user choice made between each food of the same meal.

### Learn About Seasonal Food

Using system's calendar, this option will show the user every seasonal fruit and vegetables alongside useful informations such as how to choose them, how to store them, how to cook them, some nutritional informations and benefits and also some tips.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.