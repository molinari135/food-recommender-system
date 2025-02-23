# Food Recommender System API Documentation

<a target="_blank" href="https://molinari135-food-recsys-api.hf.space/docs"><img src="https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-yellow.svg"></a>

## Overview
This document provides an overview of the Food Recommender System API, built using FastAPI. The API offers endpoints for recommending foods, generating meals, and justifying ingredient choices based on user preferences.

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Recommend Food
**Endpoint:** `/recommend`  
**Method:** `POST`  
**Description:** Recommends similar foods based on a given food item.

**Request Body:**

The request body requires:

- `food_name (str)`: the name of a food from the dataset `nutritional-facts.csv`
- `category (str)`: from the ones in `nutritional-facts.csv`
- `low_density (bool)`: the boolean value that allows to search low density similar foods, which is default, or just similar foods

```json
{
    "food_name": "Apple",
    "category": "Fruits",
    "low_density": true
}
```

**Response:**

The endpoint returns a response in a JSON format:
```json
{
    "similar_foods": [
        ["food_name", "cosine_similarity", "energy_density"]
    ]
}
```

where:

- `food_name (str)`: the name of the similar food from `nutritional-facts.csv`
- `cosine_similarity (int)`: the cosine similarity value of the food, if `low_density` is true, foods will be ordered first considering `energy_density` and then `cosine_similarity`, otherwise they will be ordered according to `cosine_similarity` only
- `energy_density`: the computed value of energy density, according to the formula $(\text{kcal} / 100g)$ considering that every nutritional facts are about 100g of food

```json
{
    "similar_foods": [
        ["Melon", 0.7164463329114419, 0.28],
        ["Watermelon", 0.7326964175293259, 0.3],
        ["Strawberry", 0.9094963059266726, 0.32],
        ["Cantaloupe", 0.700423188348832, 0.34],
        ["Honeydew", 0.9891949873765671, 0.36],
        ["Peach", 0.7785775085396299, 0.39],
        ["Prickly pear", 0.9871346141051756, 0.41],
        ["Blackberry", 0.8241823605236047, 0.43],
        ["Nectarine", 0.7865149656515035, 0.44],
        ["Plum", 0.7878549965597061, 0.46],
        ["Cranberry", 0.9849688360303036, 0.46],
        ["Clementine", 0.7191674366434099, 0.47],
        ["Orange", 0.8325730705195145, 0.47],
        ["Apricot", 0.7207069253363231, 0.48],
        ["Cherry", 0.7220235024836371, 0.5],
        ["Pineapple", 0.9970988211193901, 0.5],
        ["Raspberry", 0.9667146931857417, 0.52],
        ["Mandarin orange", 0.7502919641008965, 0.53],
        ["Currant", 0.9866449878141456, 0.56],
        ["Pear", 0.9291596079545936, 0.57],
        ["Quince", 0.9707299085387942, 0.57],
        ["Blueberry", 0.9988352415031662, 0.57],
        ["Mango", 0.7345562042500677, 0.6],
        ["Kiwifruit", 0.9855487341002364, 0.61],
        ["Grape", 0.9813355775378027, 0.67],
        ["Figs", 0.9550299168299078, 0.74],
        ["Pomegranate", 0.7162798643644303, 0.83],
        ["Banana", 0.9822656107894198, 0.89],
        ["Passion fruit", 0.7471980765769134, 0.97],
        ["Persimmon", 0.7041019190127775, 1.27],
        ["Avocado", 0.9647558795046104, 1.6],
        ["Prunes", 0.8833656387228705, 2.4],
        ["Dried fruit", 0.7428230983586804, 2.41],
        ["Dates", 0.7422920835196742, 2.82],
        ["Raisin", 0.7203458786951831, 2.99]
    ]
}
```

### 2. Recommend Cheat Meal
**Endpoint:** `/cheat`  
**Method:** `POST`  
**Description:** Recommends a cheat meal based on user fast food preferences.

**Request Body:**

The request body requires:

- `fast_food_preferences (list)`: a list with names from `Fast Foods` category in `nutritional-facts.csv`

```json
{
    "fast_food_preferences": ["Pizza", "Cheeseburger", "Hamburger"]
}
```

**Response:**

The endpoint returns a response in a JSON format:
```json
{
    "chosen_fast_food": "fast_food_name_1",
    "recommended_cheat_meal": ["fast_food_name_2", "cosine_similarity"]
}
```

where:

- `fast_food_name_1 (str)`: the name of the fast food taken as input
- `fast_food_name_2 (str)`: the name of the fast food similar to the one taken in input
- `cosine_similarity (int)`: the cosine similarity between them

```json
{
    "chosen_fast_food": "Cheeseburger",
    "recommended_cheat_meal": ["McDonald's Cheeseburger", 0.9970506395484665]
}
```

### 3. Justify Ingredients
**Endpoint:** `/justify`  
**Method:** `POST`  
**Description:** Provides a justification for choosing one meal over another based on nutritional information.

**Request Body:**

The request body requires:

- `meal_1 (list)`: a list of foods to compare in order to get the justification
- `meal_2 (list)`: a list of foods to compare in order to get the justification against the first list (they have to be one-to-one, e.g. the first element of `meal_1` will be compared with the first element of `meal_2`, and so on)

```json
{
    "meal_1": ["Pizza"],
    "meal_2": ["Pasta"]
}
```

**Response:**

The endpoint returns a response in a JSON format:

```json
{
  "justification": [
    {
      "comparison": "comparison",
      "persuasion": "persuasion",
      "food_1": "food_1",
      "food_2": "food_2",
      "score_1": "score_1",
      "score_2": "score_2"
    }
  ]
}
```

where:

- `comparison`: a message showing the macronutrient comparison between `food_1` and `food_2`
- `persuasion`: a message showing the strength and weaknesses of `food_1` and `food_2`, usually favouring `food_2`
- `food_1`: the food which is been compared against `food_2`
- `food_2`: the food which is been compared against `food_1`
- `score_1`: the score that `food_1` has won during the comparison 
- `score_2`: the score that `food_2` has won during the comparison 

The scoring system gives **1 point** to a food if:

- It has **less** calories, fats, or carbs
- It has **more** proteins, or fibers

There is a total of **5 points**, according to the number of macronutrients, which is an odd number to avoid "winning" issues.

```json
{
  "justification": [
    {
      "comparison": "**Comparing Pizza vs Pasta:**\n- Calories: Pizza has more (266), Pasta has less (131).\n- Carbs: Pizza has more (33), Pasta has less (25).\n- Fats: Pizza has more (9), Pasta has less (1).\n- Fiber: Pizza has more (2), Pasta has less (0).\n- Protein: Pizza has more (11), Pasta has less (5).\n",
      "persuasion": "\n👉 Pasta has a better macronutrient balance.\n🔥 If you're trying to lose weight, Pasta is a lighter choice.",
      "food_1": "Pizza",
      "food_2": "Pasta",
      "score_1": 2,
      "score_2": 3
    }
  ]
}
```

### 4. Generate Meals
**Endpoint:** `/generate`  
**Method:** `POST`  
**Description:** Generates a weekly meal plan based on user preferences and seasonal foods.

**Request Body:**

The request body requires:

- `food_preferences (list)`: a list of food names from `nutritional-facts.csv`
- `seasonal_preferences (list)`: a list of food names from `nutritional-facts.csv` belonging to categories `Fruits` and `Vegetables`
- `intolerances (list)`: a list of categories to remove from the dataset used for the generation

```json
{
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
        ...
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
        ...
    ],
    "intolerances": [
        "Dairy"
    ]
}
```

**Response:**

The endpoint returns a response in a JSON format:

```json
{
    "meals": {
        "Breakfast": ["original_breakfast", "alternative_breakfast"],
        "Snack": ["original_snack", "alternative_snack"],
        "Lunch": ["original_lunch", "alternative_lunch"],
        "Dinner": ["original_dinner", "alternative_dinner"]
    }
}
```

where:

- `original_breakfast (list)`: a list of food combined to obtain a breakfast using only food preferences
- `alternative_breakfast (list)`: a list of food combined to obtain a breakfast using only recommended food based on food present in the original meal
- `original_snack (list)`: a list of food combined to obtain a snack using only food preferences
- `alternative_snack (list)`: a list of food combined to obtain a snack using only recommended food based on food present in the original meal
- `original_lunch (list)`: a list of food combined to obtain a lunch using only food preferences
- `alternative_lunch (list)`: a list of food combined to obtain a lunch using only recommended food based on food present in the original meal
- `original_dinner (list)`: a list of food combined to obtain a dinner using only food preferences
- `alternative_dinner (list)`: a list of food combined to obtain a dinner using only recommended food based on food present in the original meal

```json
{
    "meals": {
        "Breakfast": [
            [
                ["Kefir", "Biscuit", "Marmalade", "Pear"],
                ["Soy yogurt", "White Bread", "Apricot jam", "Orange"]
            ],
            [
                ["Greek yogurt", "Biscuit", "Fruit preserves", "Kiwifruit"],
                ["Kefir", "White Bread", "Apricot jam", "Clementine"]
            ],
            ...
        ],
        "Snack": [
            [
                ["Coffee", "White Bread", "Fruit preserves", "Mandarin orange"],
                ["Herbal tea", "Multigrain bread", "Apricot jam", "Clementine"]
            ],
            [
                ["Greek yogurt", "Biscuit", "Fruit preserves", "Orange"],
                ["Kefir", "White Bread", "Apricot jam", "Clementine"]
            ],
            ...
        ],
        "Lunch": [
            [
                ["Pasta", "Lentil", "Olive oil", "Tomato sauce", "Potato", "Clementine"],
                ["Couscous", "Bean", "Margarine", "Salsa", "Pickled cucumber", "Orange"]
            ],
            [
                ["Wheat Bread", "Egg", "Olive oil", "Marinara sauce", "Carrot", "Kiwifruit"],
                ["Couscous", "Egg white", "Margarine", "Tomato sauce", "Pickled cucumber", "Clementine"]
            ],
            ...
        ],
        "Dinner": [
            [
                ["Pasta", "Italian sausage", "Olive oil", "Tomato sauce", "Potato", "Kiwifruit"],
                ["Couscous", "Turkey ham", "Margarine", "Salsa", "Pickled cucumber", "Clementine"]
            ],
            [
                ["Wheat Bread", "Chicken meat", "Olive oil", "Marinara sauce", "Radicchio", "Pear"],
                ["Couscous", "Rabbit Meat", "Margarine", "Tomato sauce", "Pickled cucumber", "Orange"]
            ],
            ...
        ]
    }
}
```

## Models

### RecommenderRequest
```python
class RecommenderRequest(BaseModel):
    food_name: str
    category: Optional[str]
    low_density: bool
```

### MoodRequest
```python
class MoodRequest(BaseModel):
    fast_food_preferences: List[str]
```

### JustificatorRequest
```python
class JustificatorRequest(BaseModel):
    meal_1: List[str]
    meal_2: List[str]
```

### MealGeneratorRequest
```python
class MealGeneratorRequest(BaseModel):
    food_preferences: List[str]
    seasonal_preferences: List[str]
    intolerances: Optional[List[str]]
```

## Running the API
To run the API, execute the following command:
```bash
uvicorn food_recommender_system/fastapi/api:app --reload
```

## Conclusion
This documentation provides a comprehensive overview of the Food Recommender System API. For further details, refer to the source code and comments within the implementation files.