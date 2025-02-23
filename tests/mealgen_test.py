import pytest
import pandas as pd
from food_recommender_system.profiler import UserProfiler

from food_recommender_system.mealgen import (
    generate_meal,
    generate_breakfast,
    generate_snack,
    compute_meal_calories,
    generate_weekly_meal_plan
)


@pytest.fixture
def sample_data():
    data = {
        "Category Name": [
            "Grains", "Grains", "Grains", "Grains", "Grains",
            "Vegetables", "Vegetables", "Vegetables", "Vegetables", "Vegetables",
            "Fruits", "Fruits", "Fruits", "Fruits", "Fruits",
            "Oils", "Oils", "Oils", "Oils", "Oils",
            "Sauces", "Sauces", "Sauces", "Sauces", "Sauces",
            "Dairy Breakfast", "Dairy Breakfast", "Dairy Breakfast", "Dairy Breakfast", "Dairy Breakfast",
            "Baked Products Breakfast", "Baked Products Breakfast", "Baked Products Breakfast", "Baked Products Breakfast", "Baked Products Breakfast",
            "Sweets Breakfast", "Sweets Breakfast", "Sweets Breakfast", "Sweets Breakfast", "Sweets Breakfast",
            "Nuts Breakfast", "Nuts Breakfast", "Nuts Breakfast", "Nuts Breakfast", "Nuts Breakfast",
            "Beverages", "Beverages", "Beverages", "Beverages", "Beverages",
            "Seafood", "Seafood", "Seafood", "Seafood", "Seafood",
            "Lactose-Free Dairy", "Lactose-Free Dairy", "Lactose-Free Dairy", "Lactose-Free Dairy", "Lactose-Free Dairy",
            "Eggs", "Eggs", "Eggs", "Eggs", "Eggs",
            "Legumes", "Legumes", "Legumes", "Legumes", "Legumes",
            "White Meat", "White Meat", "White Meat", "White Meat", "White Meat",
            "Cured Meat", "Cured Meat", "Cured Meat", "Cured Meat", "Cured Meat",
            "Red Meat", "Red Meat", "Red Meat", "Red Meat", "Red Meat"
        ],
        "Food Name": [
            "Rice", "Wheat", "Oats", "Quinoa", "Barley",
            "Carrot", "Spinach", "Broccoli", "Bell Pepper", "Cucumber",
            "Apple", "Banana", "Orange", "Strawberry", "Blueberry",
            "Olive Oil", "Canola Oil", "Coconut Oil", "Avocado Oil", "Sunflower Oil",
            "Ketchup", "Mayonnaise", "Mustard", "Barbecue Sauce", "Soy Sauce",
            "Milk", "Yogurt", "Cheese", "Cottage Cheese", "Cream",
            "Bread", "Croissant", "Bagel", "Muffin", "Toast",
            "Chocolate", "Candy", "Honey", "Donut", "Marshmallow",
            "Almonds", "Walnuts", "Peanuts", "Cashews", "Pistachios",
            "Coffee", "Tea", "Orange Juice", "Lemonade", "Smoothie",
            "Salmon", "Shrimp", "Tuna", "Cod", "Mackerel",
            "Almond Milk", "Coconut Milk", "Soy Milk", "Lactose-Free Cheese", "Lactose-Free Yogurt",
            "Chicken Eggs", "Duck Eggs", "Quail Eggs", "Goose Eggs", "Turkey Eggs",
            "Chickpeas", "Lentils", "Black Beans", "Kidney Beans", "Peas",
            "Chicken Breast", "Turkey Breast", "Pork Tenderloin", "Chicken Thighs", "Turkey Thighs",
            "Salami", "Pepperoni", "Prosciutto", "Bacon", "Sausage",
            "Beef Steak", "Lamb Chops", "Pork Ribs", "Ground Beef", "Lamb Shank"
        ],
        "Calories": [
            130, 339, 389, 120, 130,
            41, 23, 55, 31, 16,
            52, 89, 62, 32, 45,
            884, 884, 862, 112, 680,
            42, 59, 80, 150, 70,
            42, 59, 402, 265, 406,
            250, 546, 394, 304, 576,
            654, 567, 1, 2, 100,
            576, 400, 320, 150, 230,
            116, 144, 208, 86, 77,
            200, 120, 150, 100, 180,
            30, 60, 50, 90, 120,
            50, 80, 70, 60, 90,
            180, 200, 210, 180, 190,
            250, 200, 220, 180, 210,
            300, 350, 320, 290, 310,
            400, 450, 350, 420, 380
        ]
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_servings():
    return {
        "Grains": {"serving_size": 100, "frequency_per_week": 7},
        "Vegetables": {"serving_size": 100, "frequency_per_week": 7},
        "Fruits": {"serving_size": 100, "frequency_per_week": 7},
        "Oils": {"serving_size": 10, "frequency_per_week": 7},
        "Sauces": {"serving_size": 20, "frequency_per_week": 7},
        "Dairy Breakfast": {"serving_size": 200, "frequency_per_week": 7},
        "Baked Products Breakfast": {"serving_size": 50, "frequency_per_week": 7},
        "Sweets Breakfast": {"serving_size": 30, "frequency_per_week": 7},
        "Nuts Breakfast": {"serving_size": 30, "frequency_per_week": 7},
        "Beverages": {"serving_size": 250, "frequency_per_week": 7},
        "Seafood": {"serving_size": 100, "frequency_per_week": 3},
        "Lactose-Free Dairy": {"serving_size": 200, "frequency_per_week": 7},
        "Dairy": {"serving_size": 200, "frequency_per_week": 7},
        "Eggs": {"serving_size": 50, "frequency_per_week": 7},
        "Legumes": {"serving_size": 100, "frequency_per_week": 7},
        "White Meat": {"serving_size": 150, "frequency_per_week": 7},
        "Cured Meat": {"serving_size": 100, "frequency_per_week": 3},
        "Red Meat": {"serving_size": 150, "frequency_per_week": 3},
    }


@pytest.fixture
def mock_user_profiler(mocker):
    mock = mocker.Mock(spec=UserProfiler)

    # Update food preferences with a subset of the available foods
    mock.get_food_preferences.return_value = [
        "Rice", "Carrot", "Spinach", "Apple", "Olive Oil",
        "Ketchup", "Milk", "Bread", "Chocolate", "Almonds", "Coffee",
        "Wheat", "Oats", "Quinoa", "Barley", "Banana", "Orange",
        "Canola Oil", "Coconut Oil", "Avocado Oil", "Sunflower Oil",
        "Mayonnaise", "Mustard", "Barbecue Sauce", "Soy Sauce", "Yogurt",
        "Cheese", "Cottage Cheese", "Cream", "Croissant", "Bagel",
        "Muffin", "Toast", "Candy", "Honey", "Donut", "Marshmallow",
        "Walnuts", "Peanuts", "Cashews", "Pistachios", "Tea", "Lemonade",
        "Salmon", "Shrimp", "Tuna", "Cod", "Mackerel",
        "Almond Milk", "Coconut Milk", "Soy Milk", "Lactose-Free Cheese", "Lactose-Free Yogurt",
        "Chicken Eggs", "Duck Eggs", "Quail Eggs", "Goose Eggs", "Turkey Eggs",
        "Chickpeas", "Lentils", "Black Beans", "Kidney Beans", "Peas",
        "Chicken Breast", "Turkey Breast", "Pork Tenderloin", "Chicken Thighs", "Turkey Thighs",
        "Salami", "Pepperoni", "Prosciutto", "Bacon", "Sausage",
        "Beef Steak", "Lamb Chops", "Pork Ribs", "Ground Beef", "Lamb Shank"
    ]

    # Update seasonal preferences with food that may be seasonally relevant
    mock.get_seasonal_preferences.return_value = [
        "Carrot", "Apple", "Spinach", "Banana", "Orange", "Strawberry"
    ]

    # No intolerances are provided in this case, but you can add some if needed
    mock.get_intolerances.return_value = []

    return mock


def test_generate_meal(sample_data):
    preferences_df = sample_data
    filtered_df = sample_data
    category = "Vegetables"
    meal, similar_meal = generate_meal(preferences_df, filtered_df, category)
    assert len(meal) == 6
    assert len(similar_meal) == 6


def test_generate_breakfast(sample_data):
    preferences_df = sample_data
    filtered_df = sample_data
    breakfast, similar_breakfast = generate_breakfast(preferences_df, filtered_df)
    assert len(breakfast) == 4
    assert len(similar_breakfast) == 4


def test_generate_snack(sample_data):
    preferences_df = sample_data
    filtered_df = sample_data
    snack, similar_snack = generate_snack(preferences_df, filtered_df)
    assert len(snack) == 3
    assert len(similar_snack) == 3


def test_compute_meal_calories(sample_data, sample_servings):
    meal = ["Rice", "Carrot", "Apple"]
    df = sample_data
    servings = pd.DataFrame(sample_servings)
    calories = compute_meal_calories(meal, df, servings)
    assert calories > 0


def test_generate_weekly_meal_plan(sample_data, sample_servings, mock_user_profiler, tmp_path):
    df = sample_data
    servings = sample_servings
    filename = tmp_path / "meal_plan.json"
    meal_plan = generate_weekly_meal_plan(df, servings, mock_user_profiler, filename)
    assert len(meal_plan["Breakfast"]) == 7
    assert len(meal_plan["Snack"]) == 7
    assert len(meal_plan["Lunch"]) == 7
    assert len(meal_plan["Dinner"]) == 7
