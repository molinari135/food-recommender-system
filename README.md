# Food Recommender System
Food Recommender System with recipe and justification generation for Semantics in Intelligent Information Access and Recommender Systems @ Università degli Studi di Bari Aldo Moro, AY 2024/25

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Introduction
The Food Recommender System is designed to provide personalized recipe recommendations and generate justifications for the recommendations. This project is part of the Semantics in Intelligent Information Access course at Università degli Studi di Bari Aldo Moro for the academic year 2024/25.

## Features
- Creates or loads an existing user profile
- Personalized recipe recommendations following [EFSA](https://www.efsa.europa.eu/it) and [LARN](https://www.efsa.europa.eu/it/topics/topic/dietary-reference-values) guidelines
- Justification generation for recommendations
- Informations about seasonal fruits and vegetables(how to choose, store and eat them)
- Updates weekly meal plan taking into account user's mood

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

The system provides two standard profiles: `all_default` and `lactose_default`. You can also define a new username and it will be added automatically.
To start using the Food Recommender System, follow these steps:

```plaintext
🆔 Enter username to create or load your profile: [all_default | lactose_default]

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

### 1. Create or Load User

This option allows to load a different user or create a new one, as in the beginning of the application.

### 2. Display Current Meal and Alternatives

Using system's calendar and clock, this option will show the current meal of the day and, if needed, will ask the user to choose the actual meal by selecting a food for each section proposed. Then, it will be saved in the user's profile.

### 3. Display Weekly Meal Plan

This option will show the entire generated weekly plan with breakfasts, snacks, lunches and dinners. The first meal shown is the one generated starting from user's preferences, then it will show an alternative version with a lower energy density (which is the standardized ratio between calories and weight). It will also display the actual user choice made between each food of the same meal.

### 4. Learn About Seasonal Food

Using system's calendar, this option will show the user every seasonal fruit and vegetables alongside useful informations such as how to choose them, how to store them, how to cook them, some nutritional informations and benefits and also some tips.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.