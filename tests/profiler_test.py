import pytest
import os
import json
from food_recommender_system.profiler import UserProfiler


@pytest.fixture
def user_profiler():
    return UserProfiler()


def test_set_intolerances(user_profiler):
    user_profiler.set_intolerances("Lactose")
    assert user_profiler.get_intolerances() == [["Dairy", "Dairy Breakfast"]]

    user_profiler.set_intolerances("Gluten")
    assert user_profiler.get_intolerances() == [["Dairy", "Dairy Breakfast"], ["Grains", "Baked Products", "Baked Products Breakfast"]]


def test_set_food_preferences(user_profiler):
    food_list = ["Pizza", "Pasta"]
    user_profiler.set_food_preferences(food_list)
    assert user_profiler.get_food_preferences() == food_list


def test_set_seasonal_preferences(user_profiler):
    seasonal_list = ["Strawberries", "Pumpkin"]
    user_profiler.set_seasonal_preferences(seasonal_list)
    assert user_profiler.get_seasonal_preferences() == seasonal_list


def test_set_meals(user_profiler):
    meals = {"breakfast": "Pancakes", "lunch": "Salad"}
    user_profiler.set_meals(meals)
    assert user_profiler.get_meals() == meals


def test_set_used_jolly(user_profiler):
    user_profiler.set_used_jolly(True)
    assert user_profiler.get_used_jolly() is True


def test_save_and_load_profile(tmp_path, user_profiler):
    filename = tmp_path / "test_profile.json"
    user_profiler.set_intolerances("Lactose")
    user_profiler.set_food_preferences(["Pizza", "Pasta"])
    user_profiler.set_seasonal_preferences(["Strawberries", "Pumpkin"])
    user_profiler.set_meals({"breakfast": "Pancakes", "lunch": "Salad"})
    user_profiler.set_used_jolly(True)
    user_profiler.save_profile(filename)

    loaded_profiler = UserProfiler.load_profile(filename)
    assert loaded_profiler.get_intolerances() == [["Dairy", "Dairy Breakfast"]]
    assert loaded_profiler.get_food_preferences() == ["Pizza", "Pasta"]
    assert loaded_profiler.get_seasonal_preferences() == ["Strawberries", "Pumpkin"]
    assert loaded_profiler.get_meals() == {"breakfast": "Pancakes", "lunch": "Salad"}
    assert loaded_profiler.get_used_jolly() is True


def test_check_profile(tmp_path):
    filename = tmp_path / "test_profile.json"
    UserProfiler.check_profile(filename)
    assert os.path.exists(filename)


def test_create_new_profile(tmp_path):
    filename = tmp_path / "test_profile.json"
    UserProfiler.create_new_profile(filename)
    assert os.path.exists(filename)
    with open(filename, "r") as file:
        data = json.load(file)
        assert data == {
            "intolerances": [],
            "food_preferences": [],
            "seasonal_preferences": [],
            "meals": {},
            "used_jolly": False
        }
