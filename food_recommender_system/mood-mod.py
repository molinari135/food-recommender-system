import datetime
import random
import pandas as pd
from profiler import UserProfiler  # Assicurati che il file 'user_profiler.py' contenga la classe UserProfiler

# Simulazione di dataset di preferenze dell'utente (sostituisci con i tuoi dati reali)
profiler = UserProfiler()
user = profiler.load_profile("user_profile.json")
user_preferences = user.get_food_preferences()
user_meals = user.get_meals()

# Creazione del profilo utente
dataset_keys = user_preferences["Food Name"].unique()
user = UserProfiler()
user.add_intolerance("dairy")
user.set_food_preferences(["Apple", "Carrot", "Pasta"], dataset_keys)
user.save_profile()  # Salva il profilo iniziale

# Check what day of the week is today
today_day_of_week = datetime.datetime.now().weekday()  # Monday is 0 and Sunday is 6
print("Today lunch is:", lunches[today_day_of_week][0])

# Ask the user if today is happy or not
is_happy = input("Is today a happy day? (yes/no): ").lower() == 'yes'

if not is_happy:
    # Change today's lunch with a fast food
    fast_food = random.choice(user_preferences[user_preferences["Category Name"] == "Fast Foods"]["Food Name"].to_list())
    
    # Clear today's lunch
    new_lunch = [fast_food]
    del lunches[today_day_of_week]
    
    # Trova alimenti simili (se ci sono)
    similar_foods = find_similar_food(user_preferences, food_name=fast_food, n=1, same_category=False, low_density_food=True)
    if similar_foods:
        new_lunch.append(similar_foods[0][0])
    
    # Aggiorna il pranzo con il nuovo piatto
    lunches.insert(today_day_of_week, new_lunch)
    
    # Memorizza l'uso del "jolly"
    new_user.set_used_jolly(True)
else:
    new_user.set_used_jolly(False)

# Salva il profilo aggiornato dell'utente
new_user.save_profile()

# Mostra il pranzo aggiornato
if new_user.used_jolly:
    print(f"Today's lunch has been changed: {lunches[today_day_of_week]}")
else:
    print(f"Today's lunch remains: {lunches[today_day_of_week]}")
