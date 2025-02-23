import pytest
import pandas as pd
import json
from food_recommender_system.dataloader import DataLoader

# Sample data for testing
sample_data = {
    "Food Name": ["Apple", "Banana", "Carrot"],
    "Category Name": ["Fruit", "Fruit", "Vegetable"],
    "Calories": [52, 89, 41],
    "Protein": [0.3, 1.1, 0.9]
}


@pytest.fixture
def sample_df():
    return pd.DataFrame(sample_data)


@pytest.fixture
def dataloader():
    return DataLoader()


def test_load_csv(dataloader, mocker):
    mocker.patch("pandas.read_csv", return_value=pd.DataFrame(sample_data))
    df = dataloader.load_csv("sample.csv")
    assert not df.empty
    assert list(df.columns) == ["Food Name", "Category Name", "Calories", "Protein"]


def test_load_json(dataloader, mocker):
    mock_data = {"key": "value"}
    mocker.patch("builtins.open", mocker.mock_open(read_data=json.dumps(mock_data)))
    data = dataloader.load_json("sample.json")
    assert data == mock_data


def test_filter_categories(sample_df):
    filtered_df = DataLoader.filter_categories(sample_df, ["Fruit"])
    assert len(filtered_df) == 1
    assert filtered_df.iloc[0]["Food Name"] == "Carrot"


def test_fill_missing_values(sample_df):
    sample_df.loc[1, "Calories"] = None
    DataLoader.fill_missing_values(sample_df, fill_value=0)
    assert sample_df.loc[1, "Calories"] == 0


def test_get_nutritional_info(sample_df):
    nutritional_info = DataLoader.get_nutritional_info(sample_df, "Apple")
    assert nutritional_info is not None
    assert nutritional_info["Calories"].values[0] == 52


def test_compute_energy_density(sample_df):
    category, density = DataLoader.compute_energy_density(sample_df, "Apple")
    assert category == "Low"
    assert density == 0.52


def test_get_food_category(sample_df):
    category = DataLoader.get_food_category(sample_df, "Apple")
    assert category == "Fruit"
