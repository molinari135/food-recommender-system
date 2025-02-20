from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from numpy.linalg import norm
from pathlib import Path
import pandas as pd
import numpy as np
import uvicorn
import random
import json
import os
import logging

import food_recommender_system.fastapi.utils as utils

app = FastAPI()


# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load CSV dataset
BASE_PATH = Path(os.path.join(os.getcwd(), 'data'))
RAW_DATA_PATH = Path(os.path.join(BASE_PATH, 'raw'))

try:
    food_dataset = pd.read_csv(Path(RAW_DATA_PATH) / "nutritional-facts.csv")
    food_dataset.fillna(0, inplace=True)
    food_dataset = food_dataset[~food_dataset['Category Name'].isin(utils.EXCLUDED_CATEGORIES)]
    logger.info("Successfully loaded nutritional-facts.csv dataset.")
    logger.info("This dataset has these categories: %s", food_dataset["Category Name"].unique())
except Exception as e:
    logger.error(f"Error loading nutritional-facts.csv: {e}")

# Load JSON dataset
try:
    with open(Path(RAW_DATA_PATH) / "food-servings.json", "r", encoding="utf-8") as f:
        servings = json.load(f)
    logger.info("Successfully loaded food-servings.json dataset.")
except Exception as e:
    logger.error(f"Error loading food-servings.json: {e}")

try:
    with open(Path(RAW_DATA_PATH) / "food-seasonality.json", "r", encoding="utf-8") as f:
        seasonality = json.load(f)
    logger.info("Successfully loaded food-seasonality.json dataset.")
except Exception as e:
    logger.error(f"Error loading food-seasonality.json: {e}")


class RecommenderRequest(BaseModel):
    food_name: str = Field(
        ...,
        title="Food Name",
        description="The name of the single food item to get recommendations for.",
        example="Apple"
    )
    category: Optional[str] = Field(
        None,
        title="Food Category",
        description="Optional food category for filtering the recommendations.",
        example="Fruits"
    )
    low_density: bool = Field(
        True,
        title="Low Density",
        description="Flag to filter foods with low caloric density.",
        example=True
    )


class MoodRequest(BaseModel):
    fast_food_preferences: List[str] = Field(
        ...,
        title="Fast Food Preferences",
        description="A list of fast food items that the user prefers.",
        example=["Pizza", "Cheeseburger", "Hamburger"]
    )


class JustificatorRequest(BaseModel):
    meal_1: List[str] = Field(
        ...,
        title="Name of the food item in the meal",
        description="The name of a single food item in the meal to be compared.",
        example=["Pizza"]
    )
    meal_2: List[str] = Field(
        ...,
        title="Name of the other food item in the meal",
        description="The name of a single food item in the meal to be compared.",
        example=["Pasta"]
    )


class MealGeneratorRequest(BaseModel):
    food_preferences: List[str] = Field(
        ...,
        title="Food Preferences",
        description="A list of food items that the user prefers.",
        example=[
            "Cod",
            "Fish sticks",
            "Mussels",
            "Tuna",
            "Salmon",
            "Provolone",
            "Swiss cheese",
            "Parmigiano-Reggiano",
            "Cheese",
            "Ricotta",
            "Mozzarella",
            "Milk",
            "Yogurt",
            "Egg",
            "Olive oil",
            "Kefir",
            "Greek yogurt",
            "Chickpeas",
            "Lentil",
            "Bean",
            "Wheat Bread",
            "Pasta",
            "Rice",
            "Chicken meat",
            "Mortadella",
            "Salami",
            "Italian sausage",
            "Ham",
            "Pork",
            "Beef",
            "Marinara sauce",
            "Tomato sauce",
            "Almond",
            "Hazelnut",
            "Pistachio",
            "Walnut",
            "Almond paste",
            "Ice cream",
            "Chocolate",
            "Fruit preserves",
            "Marmalade",
            "Apple juice",
            "Orange juice",
            "Coffee",
            "Espresso",
            "Tea",
            "Biscuit",
            "White Bread",
            "Italian bread",
            "Chicken sandwich",
            "Hamburger",
            "Pizza"
        ]
    )
    seasonal_preferences: List[str] = Field(
        ...,
        title="Seasonal Preferences",
        description="A list of seasonal foods that the user prefers to include in their meals.",
        example=[
            "Apple",
            "Grapefruit",
            "Kiwifruit",
            "Orange",
            "Mandarin orange",
            "Pear",
            "Clementine",
            "Artichoke",
            "Broccoli",
            "Cabbage",
            "Carrot",
            "Cauliflower",
            "Chicory",
            "Pumpkin",
            "Turnip",
            "Potato",
            "Radicchio"
        ]
    )
    intolerances: Optional[List[str]] = Field(
        None,
        title="Food Intolerances",
        description="A list of foods the user is intolerant to. This field is optional.",
        example=["Dairy"]  # Example intolerances
    )


def generate_breakfast_or_snack(user_dataset: pd.DataFrame, food_dataset: pd.DataFrame):
    meal = []

    meal.extend([
        random.choice(
            user_dataset[user_dataset["Category Name"] == "Dairy Breakfast"]["Food Name"].to_list()
            + user_dataset[user_dataset["Category Name"] == "Lactose-Free Dairy Breakfast"]["Food Name"].to_list()
            + user_dataset[user_dataset["Category Name"] == "Beverages"]["Food Name"].to_list()
        ),
        random.choice(user_dataset[user_dataset["Category Name"] == "Baked Products Breakfast"]["Food Name"].to_list()),
        random.choice(
            user_dataset[user_dataset["Category Name"] == "Sweets Breakfast"]["Food Name"].to_list()
            + user_dataset[user_dataset["Category Name"] == "Nuts Breakfast"]["Food Name"].to_list()
        ),
        random.choice(user_dataset[user_dataset["Category Name"] == "Fruits"]["Food Name"].to_list())
    ])

    similar_meal = []
    for food_name in meal:
        food_category = utils.get_food_category(food_name, food_dataset)
        if food_category == "Fruits":
            similar_foods = get_recommendation(food_name, user_dataset)
        else:
            similar_foods = get_recommendation(food_name, food_dataset)
        similar_meal.append(similar_foods[0][0] if similar_foods else food_name)

    return meal, similar_meal


def generate_lunch_or_dinner(user_dataset: pd.DataFrame, food_dataset: pd.DataFrame, category: str) -> list:
    meal = []

    filtered_data = user_dataset[user_dataset["Category Name"] == category]

    # Check if the filtered data is not empty
    if filtered_data.empty:
        raise ValueError(f"No food items found for category: {category}")

    meal.extend([
        random.choice(
            user_dataset[user_dataset["Category Name"].isin(["Grains", "Gluten-Free Grains"])]["Food Name"].to_list()
        ),
        random.choice(user_dataset[user_dataset["Category Name"] == category]["Food Name"].to_list()),
        random.choice(user_dataset[user_dataset["Category Name"] == "Oils"]["Food Name"].to_list()),
        random.choice(user_dataset[user_dataset["Category Name"] == "Sauces"]["Food Name"].to_list()),
        random.choice(user_dataset[user_dataset["Category Name"] == "Vegetables"]["Food Name"].to_list()),
        random.choice(user_dataset[user_dataset["Category Name"] == "Fruits"]["Food Name"].to_list())
    ])

    similar_meal = []
    for food_name in meal:
        food_category = utils.get_food_category(food_name, food_dataset)

        if food_category != "Oils":
            if food_category == "Fruits":
                similar_foods = get_recommendation(food_name, user_dataset)
            else:
                similar_foods = get_recommendation(food_name, food_dataset)
            similar_meal.append(similar_foods[0][0] if similar_foods else food_name)

    return meal, similar_meal


def get_recommendation(food_name: str, food_dataset: pd.DataFrame, category: Optional[str] = None, low_density: bool = True):

    food_category = category or utils.get_food_category(food_name, food_dataset)

    if food_category is None:
        raise HTTPException(status_code=404, detail=f"Error: '{food_name}' category not found.")

    food_A = utils.get_nutritional_info(food_name, food_dataset).to_numpy().flatten()
    similar_foods = []

    for _, row in food_dataset[food_dataset["Category Name"] == food_category].iterrows():
        other_food = row["Food Name"]
        if other_food != food_name:
            food_B = row.drop(labels=["Food Name", "Category Name"]).to_numpy().flatten()

            norm_A = norm(food_A)
            norm_B = norm(food_B)

            similarity = 0 if norm_A == 0 or norm_B == 0 else np.dot(food_A, food_B) / (norm_A * norm_B)
            similar_foods.append((other_food, similarity))

    similar_foods.sort(key=lambda x: x[1], reverse=True)

    if low_density:
        # First, compute energy density for each food
        similar_foods = [(food, similarity, utils.compute_energy_density(food, food_dataset)) for food, similarity in similar_foods]
        # Sort by energy density (ascending) and then by similarity
        similar_foods.sort(key=lambda x: (x[2] if x[2] is not None else float('inf'), x[1]))

    return similar_foods


def get_justification(meal_1: list, meal_2: list, food_dataset: pd.DataFrame, verbose: bool = True):
    df = food_dataset.copy()

    if len(meal_1) != len(meal_2):
        raise HTTPException(status_code=400, detail="Error: The two meals should have the same number of items for a fair comparison.")

    justification_results = []

    # Iterate over paired foods from both meals
    for food_1, food_2 in zip(meal_1, meal_2):
        # Get nutritional information for both foods
        food_1_info = utils.get_nutritional_info(food_1, df, only_numbers=False)
        food_2_info = utils.get_nutritional_info(food_2, df, only_numbers=False)

        # If either food has missing nutritional information, raise an error
        if food_1_info.empty or food_2_info.empty:
            raise HTTPException(status_code=404, detail=f"Error: Nutritional information for '{food_1}' or '{food_2}' is missing.")

        # Initialize the comparison string
        comparison = f"**Comparing {food_1} vs {food_2}:**\n" if verbose else ""

        # Extract macronutrient values
        food_1_info = np.array(food_1_info[utils.MACRONUTRIENTS])[0]
        food_2_info = np.array(food_2_info[utils.MACRONUTRIENTS])[0]

        # Initialize persuasion string and score for each food
        persuasion = ""
        score_1 = 0
        score_2 = 0

        # Compare macronutrients
        for i, nutrient in enumerate(utils.MACRONUTRIENTS):
            f1_value = int(food_1_info[i]) if pd.notna(food_1_info[i]) else 0
            f2_value = int(food_2_info[i]) if pd.notna(food_2_info[i]) else 0

            if f1_value < f2_value:
                if verbose:
                    comparison += f"- {nutrient}: {food_1} has less ({f1_value}), {food_2} has more ({f2_value}).\n"
                if nutrient in ["Calories", "Carbs", "Fats"]:
                    score_1 += 1  # Food 1 has less calories/carbs/fats
                else:
                    score_2 += 1  # Food 2 has less calories/carbs/fats
            elif f1_value > f2_value:
                if verbose:
                    comparison += f"- {nutrient}: {food_1} has more ({f1_value}), {food_2} has less ({f2_value}).\n"
                if nutrient in ["Protein", "Fiber"]:
                    score_1 += 1  # Food 1 has more protein/fiber
                else:
                    score_2 += 1  # Food 2 has more protein/fiber
            elif f1_value == f2_value:
                if verbose:
                    comparison += f"- {nutrient}: Both have the same amount ({f1_value}).\n"

        # Add persuasion based on the winning food
        if score_2 > score_1:
            persuasion += f"\n👉 {food_2} has a better macronutrient balance."
        elif score_1 > score_2:
            persuasion += f"\n👉 {food_1} is also a good option if you're looking for an alternative."

        # Additional persuasion based on specific nutrients
        if int(food_2_info[0]) < int(food_1_info[0]):
            persuasion += f"\n🔥 If you're trying to lose weight, {food_2} is a lighter choice."
        if int(food_2_info[3]) > int(food_1_info[3]):
            persuasion += f"\n🌿 {food_2} has more fiber, making it better for digestion and gut health."
        if int(food_2_info[4]) > int(food_1_info[4]):
            persuasion += f"\n💪 If you're looking to build muscle, {food_2} is the better option because it has more proteins."

        # Add comparison and persuasion to results
        justification_results.append({
            "comparison": comparison,
            "persuasion": persuasion,
            "food_1": food_1,
            "food_2": food_2,
            "score_1": score_1,
            "score_2": score_2
        })

    return justification_results


def generate_weekly_meals(user_dataset: pd.DataFrame, food_dataset: pd.DataFrame, servings: dict):
    generated_meals = {"Breakfast": [], "Snack": [], "Lunch": [], "Dinner": []}
    lunches_and_dinners = []

    df = food_dataset.copy()

    for _ in range(7):
        breakfast, similar_breakfast = generate_breakfast_or_snack(user_dataset, df)
        snack_1, similar_snack_1 = generate_breakfast_or_snack(user_dataset, df)
        snack_2, similar_snack_2 = generate_breakfast_or_snack(user_dataset, df)
        generated_meals["Breakfast"].append((breakfast, similar_breakfast))
        generated_meals["Snack"].append((snack_1, similar_snack_1))
        generated_meals["Snack"].append((snack_2, similar_snack_2))

    for category, info in servings.items():
        if category in utils.MEAL_GENERATION_CATEGORIES:
            count = info['frequency_per_week']
            for _ in range(count):
                meal, similar_meal = generate_lunch_or_dinner(user_dataset, df, category)
                lunches_and_dinners.append((meal, similar_meal))

    generated_meals["Lunch"] = random.sample(lunches_and_dinners, 7)
    lunches_and_dinners = [meal for meal in lunches_and_dinners if meal not in generated_meals["Lunch"]]
    generated_meals["Dinner"] = random.sample(lunches_and_dinners, 7)

    return generated_meals


@app.post("/recommend")
def recommend_food(request: RecommenderRequest):
    recommendation = get_recommendation(
        request.food_name,
        food_dataset,
        request.category,
        request.low_density
    )
    return {"similar_foods": recommendation}


@app.post("/cheat")
def recommend_cheat_meal(request: MoodRequest):
    # Pick a random fast food from preferences
    chosen_fast_food = random.choice(request.fast_food_preferences)
    recommendation = get_recommendation(chosen_fast_food, food_dataset, low_density=False)

    if not recommendation:
        raise HTTPException(status_code=404, detail="No similar cheat meal found based on the selected fast food.")

    return {
        "chosen_fast_food": chosen_fast_food,
        "recommended_cheat_meal": recommendation[0]
    }


@app.post("/justify")
def justificate_ingredients(request: JustificatorRequest):
    justification = get_justification(
        request.meal_1,
        request.meal_2,
        food_dataset
    )
    return {"justification": justification}


@app.post("/generate")
def generate_meals(request: MealGeneratorRequest):
    df = food_dataset.copy()
    user_preferences = request.food_preferences + request.seasonal_preferences
    user_dataset = df[df["Food Name"].isin(user_preferences)]

    # if request.intolerances != []:
    #     user_dataset = user_dataset[~user_dataset['Category Name'].isin(request.intolerances)]

    meals = generate_weekly_meals(user_dataset, food_dataset, servings)
    return {"meals": meals}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
