import os

# Paths
BASE_PATH = os.path.join(os.getcwd(), 'data')
RAW_DATA_PATH = os.path.join(BASE_PATH, 'raw')
PROCESSED_DATA_PATH = os.path.join(BASE_PATH, 'processed')
SEASONALITY_FILE = os.path.join(RAW_DATA_PATH, 'food-seasonality.json')
NUTRITIONAL_FACTS_FILE = os.path.join(RAW_DATA_PATH, 'nutritional-facts.csv')
USER_PROFILE_FILE = os.path.join(PROCESSED_DATA_PATH, 'user_profile.json')

EXCLUDED_CATEGORIES = [
    "Baby Foods", "Meals, Entrees, and Side Dishes", "Soups", "Spices", "Fruits", "Vegetables", "Greens"
]

PREFERENCES = {
    "no_intolerances": {
        "Baked Products": ["Italian bread", "Focaccia, Crackers"],
        "Baked Products Breakfast": ["White Bread, Biscuit"],
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
        "Baked Products Breakfast": ["White Bread, Biscuit"],
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
