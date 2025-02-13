import os
from pathlib import Path

# Paths
BASE_PATH = Path(os.path.join(os.getcwd(), 'data'))
RAW_DATA_PATH = Path(os.path.join(BASE_PATH, 'raw'))
PROCESSED_DATA_PATH = Path(os.path.join(BASE_PATH, 'processed'))

MACRONUTRIENTS = ["Calories", "Carbs", "Fats", "Fiber", "Protein"]
EXCLUDED_CATEGORIES = ["Baby Foods", "Meals, Entrees, and Side Dishes", "Soups", "Spices", "Fruits", "Vegetables", "Greens"]

LACTOSE_INTOLERANCE = ["Dairy", "Dairy Breakfast"]
GLUTEN_INTOLERANCE = ["Grains", "Baked Products", "Baked Products Breakfast"]
LACTOSE_AND_GLUTEN_INTOLERANCE = LACTOSE_INTOLERANCE + GLUTEN_INTOLERANCE

MEAL_GENERATION_CATEGORIES = ["Seafood", "Lactose-Free Dairy", "Dairy", "Eggs", "Legumes", "White Meat", "Cured Meat", "Red Meat"]

PREFERENCES = {
    "no_intolerances": {
        "Baked Products": ["Italian bread", "Focaccia, Crackers"],
        "Baked Products Breakfast": ["White Bread", "Biscuit"],
        "Beverages": ["Espresso", "Tea", "Orange juice", "Apple juice", "Coffee"],
        "Cured Meat": ["Italian sausage", "Salami", "Mortadella", "Ham"],
        "Dairy": ["Mozzarella", "Ricotta", "Cheese"],
        "Dairy Breakfast": ["Yogurt", "Milk"],
        "Eggs": ["Egg"],
        "Fast Foods": ["Hamburger", "Chicken sandwich", "Pizza"],
        "Gluten-Free Grains": ["Rice"],
        "Grains": ["Pasta", "Wheat Bread"],
        "Lactose-Free Dairy": ["Provolone", "Swiss cheese", "Parmigiano-Reggiano"],
        "Lactose-Free Dairy Breakfast": ["Greek yogurt", "Kefir"],
        "Legumes": ["Chickpeas", "Lentil", "Bean"],
        "Nuts": ["Walnut", "Hazelnut", "Pistachio", "Almond"],
        "Nuts Breakfast": ["Almond paste"],
        "Oils": ["Olive oil"],
        "Red Meat": ["Beef", "Pork"],
        "Sauces": ["Tomato sauce", "Marinara sauce"],
        "Seafood": ["Salmon", "Tuna", "Fish sticks", "Cod", "Mussels"],
        "Sweets": ["Chocolate", "Ice cream"],
        "Sweets Breakfast": ["Marmalade", "Fruit preserves"],
        "White Meat": ["Chicken meat"]
    },
    "lactose_intolerance": {
        "Baked Products": ["Italian bread", "Focaccia, Crackers"],
        "Baked Products Breakfast": ["White Bread", "Biscuit"],
        "Beverages": ["Espresso", "Tea", "Orange juice", "Apple juice", "Coffee"],
        "Cured Meat": ["Italian sausage", "Salami", "Mortadella", "Ham"],
        "Eggs": ["Egg"],
        "Fast Foods": ["Hamburger", "Chicken sandwich", "Pizza"],
        "Gluten-Free Grains": ["Rice"],
        "Grains": ["Pasta", "Wheat Bread"],
        "Lactose-Free Dairy": ["Provolone", "Swiss cheese", "Parmigiano-Reggiano"],
        "Lactose-Free Dairy Breakfast": ["Greek yogurt", "Kefir"],
        "Legumes": ["Chickpeas", "Lentil", "Bean"],
        "Nuts": ["Walnut", "Hazelnut", "Pistachio", "Almond"],
        "Nuts Breakfast": ["Almond paste"],
        "Oils": ["Olive oil"],
        "Red Meat": ["Beef", "Pork"],
        "Sauces": ["Tomato sauce", "Marinara sauce"],
        "Seafood": ["Salmon", "Tuna", "Fish sticks", "Cod", "Mussels"],
        "Sweets": ["Crème caramel", "Chocolate", "Ice cream"],
        "Sweets Breakfast": ["Marmalade", "Fruit preserves"],
        "White Meat": ["Chicken meat"]
    },
    "gluten_intolerance": {
        "Beverages": ["Espresso", "Tea", "Orange juice", "Apple juice", "Coffee", "Milk"],
        "Cured Meat": ["Italian sausage", "Salami", "Mortadella", "Ham"],
        "Eggs": ["Egg"],
        "Fast Foods": ["Hamburger", "Chicken sandwich", "Pizza"],
        "Gluten-Free Grains": ["Rice"],
        "Lactose-Free Dairy": ["Provolone", "Swiss cheese", "Parmigiano-Reggiano"],
        "Lactose-Free Dairy Breakfast": ["Greek yogurt", "Kefir"],
        "Legumes": ["Chickpeas", "Lentil", "Bean"],
        "Nuts": ["Walnut", "Hazelnut", "Pistachio", "Almond"],
        "Nuts Breakfast": ["Almond paste"],
        "Oils": ["Olive oil"],
        "Red Meat": ["Beef", "Pork"],
        "Sauces": ["Tomato sauce", "Marinara sauce"],
        "Seafood": ["Salmon", "Tuna", "Fish sticks", "Cod", "Mussels"],
        "Sweets": ["Crème caramel", "Chocolate", "Ice cream"],
        "Sweets Breakfast": ["Marmalade", "Fruit preserves"],
        "White Meat": ["Chicken meat"]
    },
    "lactose_and_gluten_intolerance": {
        "Beverages": ["Espresso", "Tea", "Orange juice", "Apple juice", "Coffee", "Milk"],
        "Cured Meat": ["Italian sausage", "Salami", "Mortadella", "Ham"],
        "Eggs": ["Egg"],
        "Fast Foods": ["Hamburger", "Chicken sandwich", "Pizza"],
        "Gluten-Free Grains": ["Rice"],
        "Lactose-Free Dairy": ["Provolone", "Swiss cheese", "Parmigiano-Reggiano"],
        "Lactose-Free Dairy Breakfast": ["Greek yogurt", "Kefir"],
        "Legumes": ["Chickpeas", "Lentil", "Bean"],
        "Nuts": ["Walnut", "Hazelnut", "Pistachio", "Almond"],
        "Nuts Breakfast": ["Almond paste"],
        "Oils": ["Olive oil"],
        "Red Meat": ["Beef", "Pork"],
        "Sauces": ["Tomato sauce", "Marinara sauce"],
        "Seafood": ["Salmon", "Tuna", "Fish sticks", "Cod", "Mussels"],
        "Sweets": ["Crème caramel", "Chocolate", "Ice cream"],
        "Sweets Breakfast": ["Marmalade", "Fruit preserves"],
        "White Meat": ["Chicken meat"]
    }
}


def get_data_file_path(filename):
    return os.path.join(BASE_PATH, filename)
