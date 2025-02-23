import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import MagicMock, patch
from food_recommender_system.recommender import get_seasonal_food, get_similar_food, ask_seasonal_preferences
from food_recommender_system.profiler import UserProfiler


@pytest.fixture
def sample_data():
    data = {
        "Food Name": ["Apple", "Banana", "Carrot", "Broccoli"],
        "Category Name": ["Fruits", "Fruits", "Vegetables", "Vegetables"],
        "Calories": [52, 89, 41, 55],
        "Carbs": [14, 23, 10, 11],
        "Fats": [0.2, 0.3, 0.2, 0.6],
        "Protein": [0.3, 1.1, 0.9, 3.7]
    }
    return pd.DataFrame(data)


@pytest.fixture
def seasonality():
    return {
        "Italy": {
            "01": ["Apple", "Carrot"],
            "02": ["Apple", "Carrot"],
            "03": ["Apple", "Carrot"],
            "04": ["Apple", "Carrot"],
            "05": ["Apple", "Carrot"],
            "06": ["Apple", "Carrot"],
            "07": ["Apple", "Carrot"],
            "08": ["Apple", "Carrot"],
            "09": ["Apple", "Carrot"],
            "10": ["Apple", "Carrot"],
            "11": ["Apple", "Carrot"],
            "12": ["Apple", "Carrot"]
        }
    }


@pytest.fixture
def user_profiler():
    profiler = MagicMock(spec=UserProfiler)
    profiler.get_intolerances.return_value = []
    return profiler


def test_get_seasonal_food(sample_data, seasonality):
    fruits, vegetables = get_seasonal_food(sample_data, seasonality, nationality="Italy")
    assert fruits == ["Apple"]
    assert vegetables == ["Carrot"]


def test_get_similar_food(sample_data):
    # Test the get_similar_food function
    similar_foods = get_similar_food(sample_data, "Apple")
    assert len(similar_foods) > 0  # Ensure there is at least one similar food
    assert similar_foods[0][0] == "Banana"  # Ensure the first similar food is "Banana"


def test_ask_seasonal_preferences(sample_data, seasonality, user_profiler):
    # Mocking user profile seasonal preferences methods
    user_profiler.set_seasonal_preferences = MagicMock()
    user_profiler.save_profile = MagicMock()

    filename = Path("user_profile.json")
    info_file = {
        "Apple": {"benefits": ["Rich in fiber"]},
        "Carrot": {"benefits": ["Good for eyesight"]}
    }

    # Mock input to simulate user selection for fruits and vegetables
    with patch("builtins.input", side_effect=["1", "1"]):  # Simulate selecting the first item (Apple and Carrot)
        ask_seasonal_preferences(sample_data, seasonality, user_profiler, filename, info_file)

    user_profiler.set_seasonal_preferences.assert_called_once()
    user_profiler.save_profile.assert_called_once_with(filename)


if __name__ == "__main__":
    pytest.main()
