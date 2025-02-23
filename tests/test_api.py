from fastapi.testclient import TestClient
from food_recommender_system.fastapi.api import app

client = TestClient(app)


def test_recommend_food():
    response = client.post("/recommend", json={
        "food_name": "Apple",
        "category": "Fruits",
        "low_density": True
    })
    assert response.status_code == 200
    assert "similar_foods" in response.json()


def test_recommend_food_not_found():
    response = client.post("/recommend", json={
        "food_name": "Apples",
        "low_density": True
    })
    assert response.status_code == 404


def test_recommend_cheat_meal():
    response = client.post("/cheat", json={
        "fast_food_preferences": ["Pizza", "Cheeseburger", "Hamburger"]
    })
    assert response.status_code == 200
    assert "chosen_fast_food" in response.json()
    assert "recommended_cheat_meal" in response.json()


def test_recommend_cheat_meal_not_found():
    response = client.post("/cheat", json={
        "fast_food_preferences": ["NonExistentFastFood"]
    })
    assert response.status_code == 404


def test_justificate_ingredients():
    response = client.post("/justify", json={
        "meal_1": ["Pizza"],
        "meal_2": ["Pasta"]
    })
    assert response.status_code == 200
    assert "justification" in response.json()


def test_justificate_ingredients_mismatch():
    response = client.post("/justify", json={
        "meal_1": ["Pizza"],
        "meal_2": ["Pasta", "Salad"]
    })
    assert response.status_code == 400


def test_generate_meals():
    response = client.post("/generate", json={
        "food_preferences": [
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
        ],
        "seasonal_preferences": [
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
        ],
        "intolerances": [
            "Dairy"
        ]
    })
    assert response.status_code == 200
    assert "meals" in response.json()
