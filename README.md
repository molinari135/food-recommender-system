# Food Recommender System with Justification
> Food Recommender System with recipe and justification generation for Semantics in Intelligent Information Access and Recommender Systems @ Università degli Studi di Bari Aldo Moro, AY 2024/25

[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Static Badge](https://img.shields.io/badge/Docs-Food_RecSys-blue)](docs/)
[![Static Badge](https://img.shields.io/badge/Docs-FastAPI_API-blue)](docs/)
[![Static Badge](https://img.shields.io/badge/Docs-Streamlit_Demo-blue)](docs/)
<a target="_blank" href="https://molinari135-food-recsys-api.hf.space/docs"><img src="https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-yellow.svg"></a>
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://huggingface.co/spaces/molinari135/food-recsys-demo)


![foodrecsys](https://github.com/user-attachments/assets/0040e027-d13c-4145-a19d-3ca0138ce57d)


## Table of Contents
- [Overview](#overview)
- [Documentation](#documentation)
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Overview

The Food Recommender System is designed to provide personalized recipe recommendations and generate justifications for the recommendations. This project is part of the Semantics in Intelligent Information Access course and Recommender System course at Università degli Studi di Bari Aldo Moro for the academic year 2024/25.

The system's architecture includes multiple components, each responsible for different aspects of meal recommendation and justification. Below is a breakdown of the system's key modules and functionalities:

- **User Profiler**: Captures and updates user preferences, intolerances, and meal history.
- **Meal Generator**: Creates meals based on user preferences, available ingredients, and nutritional data.
- **Justificator**: Provides reasoning behind meal recommendations, including nutritional benefits.
- **Mood Module**: Suggests meals based on the user’s mood, e.g., recommending comfort foods if the user is stressed.
- **Seasonal Recommendations**: Encourages consumption of seasonal ingredients based on environmental and health benefits.


## Documentation

In the `docs` folder you can find the following documentation:

- `food-recsys-docs.md`: Food Recommender System Standalone Documentation
- `food-recsys-api-docs.md`: FastAPI API Documentation
- `food-recsys-demo-docs.md`: Streamlit Demo Documentation

A PDF version of every file is also available in the very same folder. These files can also be reached by clicking on the badges at the top of the page.

## Project Structure
The project is structured as follows:

```
food-recommender-system/
|
├── data/                               <-- Contains datasets and user profiles*
|   ├── processed/                      <-- Saving folder for user profiles*
|   ├── raw/                            <-- Folder with datasets used by the system*
|   |   ├── food-infos.json             <-- Informations about seasonal produces*
|   |   ├── food-seasonality.json       <-- National seasonal foods*
|   |   ├── food-servings.json          <-- LARN's italian serving sizes and frequencies*
|   |   └── nutritional-facts.csv       <-- Nutritional dataset*
|   |
├── docs/                               <-- Docs about the system, the API and the demo
|   ├── food-recsys-docs.md
|   ├── food-recsys-api-docs.md
|   └── food-recsys-dmeo-docs.md
|
├──food_recommender_system/
|   ├── demo/                           <--- Streamlit Demo folder
|   |   ├── pages/
|   |   |   ├── 1_home.py               <-- Create or Load User Profiles
|   |   |   ├── 2_user_profile.py       <-- Shows User Profile Informations
|   |   |   └── 3_meal_selection.py     <-- Select between original and recommended meals
|   |   |
|   |   └── main.py                     <-- Launches the Streamlit demo
|   |
|   ├── fastapi/                        <-- FastAPI API folder
|   |   ├── api.py                      <-- API endpoints logic
|   |   ├── main.py                     <-- Launches the API on localhost:8000
|   |   └── utils.py                    <-- Useful functions for the API
|   |
|   ├── config.py                       <-- Contains all constants and Paths*
|   ├── dataloader.py                   <-- Manages JSON, CSV and other files*
|   ├── justificator.py                 <-- Persuasion logic for recommended meals*
|   ├── main.py                         <-- Launches the standalone system with CLI interface*
|   ├── mealgen.py                      <-- Generates meals based starting from preferences*
|   ├── moodmod.py                      <-- Module related to cheat meals*
|   ├── profiler.py                     <-- Manages UserProfile objects*
|   └── recommender.py                  <-- Functions to retrieve similar foods*
|
├── references/                         <-- EFSA, CREA and LARN reference documents
|   ├── efsa-summary.pdf
|   └── porzioni-larn.pdf
|
├── LICENSE
├── Makefile
├── metrics.json                        <-- Saves statistics and ratings about the system*
├── pyproject.toml
├── README.md
├── requirements.txt
└── setup.cfg
```

> **Note**: folders and fiels with \* symbol are necessary in order to let the system work

## Features

- Create or load a user profile with preferences, intolerances and meals
- Ask for seasonal and non-seasonal preferences to generate meals
- Recommend similar food with lower energy density from the same category or not
- Once per week, ask the user if wants to have a cheat meal
- Show useful information about seasonal and local fruits and vegetables


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

### Option 1: Standalone System

[![Static Badge](https://img.shields.io/badge/Docs-Food_RecSys-blue)](docs/)
[![Static Badge](https://img.shields.io/badge/Docs-FastAPI_API-blue)](docs/)
[![Static Badge](https://img.shields.io/badge/Docs-Streamlit_Demo-blue)](docs/)

To use the Food Recommender System, run the following command:

```bash
python food_recommender_system/main.py
```

The system provides a standard profile named `default`. You can also define a new username and it will be added automatically.
The following is an example of usage of the system using the CLI interface.

> If you do not write any number during the preferences selection, the system will load default choices.

> If you do not write any number during the seasonal preference selection, the system will load every seasonal food.

Follow the on-screen instructions to get personalized recipe recommendations.

1. **Create or Load User**: This option allows to load a different user or create a new one, as in the beginning of the application.
2. **Display Current Meal and Alternatives**: Using system's calendar and clock, this option will show the current meal of the day and, if needed, will ask the user to choose the actual meal by selecting a food for each section proposed. Then, it will be saved in the user's profile.
3. **Display Weekly Meal Plan**: This option will show the entire generated weekly plan with breakfasts, snacks, lunches and dinners. The first meal shown is the one generated starting from user's preferences, then it will show an alternative version with a lower energy density (which is the standardized ratio between calories and weight). It will also display the actual user choice made between each food of the same meal.
4. **Learn About Seasonal Food**: Using your system's calendar, this option will show the user every seasonal fruit and vegetables alongside useful informations such as how to choose them, how to store them, how to cook them, some nutritional informations and benefits and also some tips.

Example of loading the profile `lactose`:

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

### Option 2: Streamlit Demo

<a target="_blank" href="https://molinari135-food-recsys-api.hf.space/docs"><img src="https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-yellow.svg"></a>
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://huggingface.co/spaces/molinari135/food-recsys-demo)

The system has a GUI demo made with **Streamlit** that can be tested by running the following command:

```bash
streamlit run food_recommender_system/demo/main.py
```

it will automatically open the demo in your browser. If you want to try the demo without installing anything, you can reach it at this [link](https://huggingface.co/spaces/molinari135/food-recsys-demo) that will redirect to Hugging Face Spaces, were it is hosted.

This demo relies on an API hosted in another Hugging Face Spaces. The **Swagger UI** can be reached at this [link](https://molinari135-food-recsys-api.hf.space/docs).

> Spaces automatically shut down after 48h of inactivity; if the system is not working or the API is "down", please send me an email at e.molinari3@studenti.uniba.it

The demo has the same functionality as the standalone version and has the following initial screen:

![alt text](image.png)

In the main page of the Streamlit demo are shown the **Recommender Performances**. They are very useful to understand how well the recommender is performing overall:

- **Win Rate**: Percentage of times the recommender system's suggestion was chosen.
- **Rejection Rate**: Percentage of times the user rejected the recommender system's suggestion.
- **Avg. Persuasion Rating**: Average rating given by the user for the persuasion message of the recommendation.

All these informations are obtained during runtime and saved in `metrics.json` file that can be accessed every time and contains the following informations:

- `recsys_wins`: number of times in which the recommended food has been chosen instead of the preferred food
- `user_wins`: number of times in which the preferred food has been chosen instead of the recommended food
- `justification_success`: for now, same as the `recsys_wins` (for future uses)
- `total_choices`: total number of choices that users have been made from the launch of the system
- `persuasion_satisfaction`: a list with ratings from 1 to 5 that express the review of the overall comparison between preferred and recommended foods

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
