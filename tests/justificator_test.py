import pytest
import pandas as pd
from food_recommender_system.profiler import UserProfiler
from unittest.mock import MagicMock

from food_recommender_system.justificator import (
    print_meal,
    print_full_week_meals,
    compare_meals,
    recommend_seasonal,
    get_current_meal
)


@pytest.fixture
def sample_dataframe():
    data = {
        'Food Name': ['Apple', 'Banana', 'Chicken', 'Broccoli'],
        'Category Name': ['Fruit', 'Fruit', 'Meat', 'Vegetable'],
        'Calories': [52, 89, 239, 55],
        'Carbs': [14, 23, 0, 11],
        'Fats': [0.2, 0.3, 14, 0.6],
        'Protein': [0.3, 1.1, 27, 3.7],
        'Fiber': [2.4, 2.6, 0, 2.6]
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_servings():
    return {
        'Fruit': {'serving_size': 100, 'tips': 'Eat fresh'},
        'Meat': {'serving_size': 150, 'tips': 'Cook thoroughly'},
        'Vegetable': {'serving_size': 200, 'tips': 'Steam for best results'}
    }


@pytest.fixture
def sample_user():
    user = MagicMock(spec=UserProfiler)
    user.get_meals.return_value = {
        "Breakfast": [
            (["Apple"], ["Banana"]),
            (["Apple"], ["Banana"]),
            (["Apple"], ["Banana"]),
            (["Apple"], ["Banana"]),
            (["Apple"], ["Banana"]),
            (["Apple"], ["Banana"]),
            (["Apple"], ["Banana"])
        ],
        "Lunch": [
            (["Chicken"], ["Broccoli"]),
            (["Chicken"], ["Broccoli"]),
            (["Chicken"], ["Broccoli"]),
            (["Chicken"], ["Broccoli"]),
            (["Chicken"], ["Broccoli"]),
            (["Chicken"], ["Broccoli"]),
            (["Chicken"], ["Broccoli"])
        ]
    }
    return user


def test_print_meal(sample_dataframe, sample_servings, capsys):
    meal = ["Apple", "Banana"]
    print_meal(meal, sample_dataframe, sample_servings)
    captured = capsys.readouterr()
    assert "- 100g of Apple (Eat fresh)" in captured.out
    assert "- 100g of Banana (Eat fresh)" in captured.out


def test_print_full_week_meals(sample_user, sample_dataframe, sample_servings, monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: 'print')
    print_full_week_meals(sample_user, sample_dataframe, sample_servings)
    captured = capsys.readouterr()
    assert "📅 Monday:" in captured.out
    assert "🍽️  Breakfast:" in captured.out
    assert "👉 Main option:" in captured.out
    assert "- 100g of Apple (Eat fresh)" in captured.out


def test_compare_meals(sample_dataframe):
    meal1 = ["Apple"]
    meal2 = ["Banana"]
    result = compare_meals(sample_dataframe, meal1, meal2, verbose=True)
    assert "Comparing Apple vs Banana:" in result[0]
    assert "Calories: Apple has less" in result[0]


def test_recommend_seasonal():
    seasonal_info = {
        'Apple': {
            'benefits': ['Rich in fiber', 'Good for heart'],
            'nutritional_intake': '52 calories per 100g'
        }
    }
    result = recommend_seasonal(seasonal_info, 'Apple')
    assert "🌿 Why choose Apple?" in result
    assert "💪 Health Benefits: Rich in fiber, Good for heart" in result


def test_get_current_meal(sample_user):
    meal_name, current_meal, current_alternative, chosen_meal = get_current_meal(sample_user, debug=True, meal_name="Breakfast")
    assert meal_name == "Breakfast"
    assert current_meal == ["Apple"]
    assert current_alternative == ["Banana"]
    assert chosen_meal is None
