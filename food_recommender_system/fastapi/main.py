import requests

API_URL = "http://127.0.0.1:8000"

food_preferences = [
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

seasonal_preferences = [
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

print(', '.join(seasonal_preferences))

intolerances = []


payload = {
    "food_preferences": food_preferences,
    "seasonal_preferences": seasonal_preferences,
    "intolerances": intolerances
}

response = requests.post(f"{API_URL}/generate", json=payload)

if response.status_code == 200:
    try:
        data = response.json()
        print(data)
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
else:
    print(f"Request failed with status code: {response.status_code}")
