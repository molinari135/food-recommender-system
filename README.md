# Food Recommender System with Justification
> Food Recommender System with recipe and justification generation for Semantics in Intelligent Information Access and Recommender Systems @ Università degli Studi di Bari Aldo Moro, AY 2024/25

[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
<a target="_blank" href="https://huggingface.co/spaces/molinari135/food-recsys-demo"><img src="https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-yellow.svg"></a>
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]()

![foodrecsys](https://github.com/user-attachments/assets/0040e027-d13c-4145-a19d-3ca0138ce57d)

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
The following is an example of usage of the system using the CLI interface.

> If you do not write any number during the preferences selection, the system will load default choices.

> If you do not write any number during the seasonal preference selection, the system will load every seasonal food.

Follow the on-screen instructions to get personalized recipe recommendations.

1. **Create or Load User**: This option allows to load a different user or create a new one, as in the beginning of the application.
2. **Display Current Meal and Alternatives**: Using system's calendar and clock, this option will show the current meal of the day and, if needed, will ask the user to choose the actual meal by selecting a food for each section proposed. Then, it will be saved in the user's profile.
3. **Display Weekly Meal Plan**: This option will show the entire generated weekly plan with breakfasts, snacks, lunches and dinners. The first meal shown is the one generated starting from user's preferences, then it will show an alternative version with a lower energy density (which is the standardized ratio between calories and weight). It will also display the actual user choice made between each food of the same meal.
4. **Learn About Seasonal Food**: Using system's calendar, this option will show the user every seasonal fruit and vegetables alongside useful informations such as how to choose them, how to store them, how to cook them, some nutritional informations and benefits and also some tips.

Example of loading standard profile `lactose`:

![Screenshot 2025-02-17 094612](https://github.com/user-attachments/assets/e2178773-a4fa-48d4-8212-0b3719e1ad0d)

Example of menu showing after creating or loading a profile:

![Screenshot 2025-02-17 104327](https://github.com/user-attachments/assets/a270380a-1be8-4b98-bcdc-dbecb929d04f)

Printing the generated weekly meal plan:

![Screenshot 2025-02-17 094511](https://github.com/user-attachments/assets/9c12d766-a17b-4d49-92c9-1afa35fe2e0d)

Or creating the CSV version of the plan:

![Screenshot 2025-02-17 100059](https://github.com/user-attachments/assets/de8806b0-eba8-46fc-9258-1c723903606f)

Example of current meal and justificator triggering:

![Screenshot 2025-02-17 093745](https://github.com/user-attachments/assets/309caacc-526e-4346-8be3-2d7fdede7139)

Seasonality function that shows all seasonal produces for the current month:

![Screenshot 2025-02-17 093709](https://github.com/user-attachments/assets/4ef69d3f-d867-4f44-ab45-e09a0c304734)

Example of information provided for a seasonal food:

![Screenshot 2025-02-17 093728](https://github.com/user-attachments/assets/96017f21-3392-410c-b31e-e2b3013669c2)

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
