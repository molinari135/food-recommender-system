import pytest
from unittest.mock import MagicMock, patch
from food_recommender_system.moodmod import change_meal, reset_jolly_if_new_week
from food_recommender_system.profiler import UserProfiler
from pathlib import Path
import pandas as pd


@pytest.fixture
def user_profiler():
    user = MagicMock(spec=UserProfiler)
    user.get_meals.return_value = {
        "Lunch": [["Meal1", "Meal2", "Meal3"] for _ in range(7)],
        "Dinner": [["Meal1", "Meal2", "Meal3"] for _ in range(7)]
    }
    user.get_used_jolly.return_value = False
    return user


@pytest.fixture
def food_dataframe():
    data = {
        "Food Name": ["Burger", "Pizza", "Fries"],
        "Category Name": ["Fast Foods", "Fast Foods", "Fast Foods"]
    }
    return pd.DataFrame(data)


@pytest.fixture
def filename():
    return Path("/path/to/profile.json")


@patch('builtins.input', lambda *args: 'yes')
@patch('food_recommender_system.moodmod.get_current_meal')
@patch('food_recommender_system.moodmod.datetime')
def test_change_meal_stressed(mock_datetime, mock_get_current_meal, user_profiler, food_dataframe, filename):
    mock_datetime.now.return_value.weekday.return_value = 0
    change_meal(user_profiler, food_dataframe, "Lunch", filename)
    user_profiler.set_used_jolly.assert_called_once_with(True)
    user_profiler.save_profile.assert_called()


@patch('builtins.input', lambda *args: 'no')
@patch('food_recommender_system.moodmod.datetime')
def test_change_meal_not_stressed(mock_datetime, user_profiler, food_dataframe, filename):
    mock_datetime.now.return_value.weekday.return_value = 0
    change_meal(user_profiler, food_dataframe, "Lunch", filename)
    user_profiler.set_used_jolly.assert_not_called()
    user_profiler.save_profile.assert_not_called()


@patch('food_recommender_system.moodmod.datetime')
def test_reset_jolly_if_new_week(mock_datetime, user_profiler):
    mock_datetime.now.return_value.weekday.return_value = 0
    mock_datetime.now.return_value.hour = 0
    mock_datetime.now.return_value.minute = 0
    reset_jolly_if_new_week(user_profiler)
    user_profiler.set_used_jolly.assert_called_once_with(False)


@patch('food_recommender_system.moodmod.datetime')
def test_reset_jolly_if_not_new_week(mock_datetime, user_profiler):
    mock_datetime.now.return_value.weekday.return_value = 1
    reset_jolly_if_new_week(user_profiler)
    user_profiler.set_used_jolly.assert_not_called()
