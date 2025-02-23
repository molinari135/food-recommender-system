from pathlib import Path
import os
import sys
from food_recommender_system.config import BASE_PATH, RAW_DATA_PATH, PROCESSED_DATA_PATH, MACRONUTRIENTS, EXCLUDED_CATEGORIES, LACTOSE_INTOLERANCE, GLUTEN_INTOLERANCE, LACTOSE_AND_GLUTEN_INTOLERANCE, MEAL_GENERATION_CATEGORIES, PREFERENCES, get_data_file_path

# Add the path to the config module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'food_recommender_system')))


def test_base_path():
    expected_path = Path(os.path.join(os.getcwd(), 'data'))
    assert BASE_PATH == expected_path


def test_raw_data_path():
    expected_path = Path(os.path.join(BASE_PATH, 'raw'))
    assert RAW_DATA_PATH == expected_path


def test_processed_data_path():
    expected_path = Path(os.path.join(BASE_PATH, 'processed'))
    assert PROCESSED_DATA_PATH == expected_path


def test_macronutrients():
    expected_macronutrients = ["Calories", "Carbs", "Fats", "Fiber", "Protein"]
    assert MACRONUTRIENTS == expected_macronutrients


def test_excluded_categories():
    expected_categories = ["Baby Foods", "Meals, Entrees, and Side Dishes", "Soups", "Spices", "Fruits", "Vegetables", "Greens"]
    assert EXCLUDED_CATEGORIES == expected_categories


def test_lactose_intolerance():
    expected_lactose_intolerance = ["Dairy", "Dairy Breakfast"]
    assert LACTOSE_INTOLERANCE == expected_lactose_intolerance


def test_gluten_intolerance():
    expected_gluten_intolerance = ["Grains", "Baked Products", "Baked Products Breakfast"]
    assert GLUTEN_INTOLERANCE == expected_gluten_intolerance


def test_lactose_and_gluten_intolerance():
    expected_combined_intolerance = LACTOSE_INTOLERANCE + GLUTEN_INTOLERANCE
    assert LACTOSE_AND_GLUTEN_INTOLERANCE == expected_combined_intolerance


def test_meal_generation_categories():
    expected_categories = ["Seafood", "Lactose-Free Dairy", "Dairy", "Eggs", "Legumes", "White Meat", "Cured Meat", "Red Meat"]
    assert MEAL_GENERATION_CATEGORIES == expected_categories


def test_preferences_no_intolerances():
    assert "no_intolerances" in PREFERENCES
    assert "Baked Products" in PREFERENCES["no_intolerances"]
    assert "Italian bread" in PREFERENCES["no_intolerances"]["Baked Products"]


def test_preferences_lactose_intolerance():
    assert "lactose_intolerance" in PREFERENCES
    assert "Baked Products" in PREFERENCES["lactose_intolerance"]
    assert "Italian bread" in PREFERENCES["lactose_intolerance"]["Baked Products"]


def test_preferences_gluten_intolerance():
    assert "gluten_intolerance" in PREFERENCES
    assert "Beverages" in PREFERENCES["gluten_intolerance"]
    assert "Espresso" in PREFERENCES["gluten_intolerance"]["Beverages"]


def test_preferences_lactose_and_gluten_intolerance():
    assert "lactose_and_gluten_intolerance" in PREFERENCES
    assert "Beverages" in PREFERENCES["lactose_and_gluten_intolerance"]
    assert "Espresso" in PREFERENCES["lactose_and_gluten_intolerance"]["Beverages"]


def test_get_data_file_path():
    filename = "test_file.csv"
    expected_path = os.path.join(BASE_PATH, filename)
    assert get_data_file_path(filename) == expected_path
