# HACKATHON FALL SEMESTER 2024 #
# DYLAN KOHN, JONATHAN NELSON, JONATHAN ASCONA #
# 10/18/24 - 10/19/24)


import requests
import json
import os

# Your Spoonacular API key
API_KEY = "9d85a62254ac4052b9ff54e5d8425688"

# File to store saved recipes
SAVED_RECIPES_FILE = "saved_recipes.json"

# Function to save ingredients to a list and store them in a text file
def add_ingredients_to_list(ingredients, filename="ingredients.txt"):
    with open(filename, 'a') as file:
        file.write(", ".join(ingredients) + "\n")
    print(f"Ingredients '{', '.join(ingredients)}' have been added to the list.")

# Function to load previously entered ingredients from a text file
def load_ingredients_from_file(filename="ingredients.txt"):
    try:
        with open(filename, 'r') as file:
            content = file.readlines()
            ingredients = [line.strip() for line in content]
            return ingredients
    except FileNotFoundError:
        return []

# Function to fetch recipes based on ingredients
def get_recipes(ingredients):
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=5&apiKey=9d85a62254ac4052b9ff54e5d8425688"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch recipes. Status code: {response.status_code}")
        return None

# Function to fetch recipe details, including instructions and nutrition
def get_recipe_details(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?includeNutrition=true&apiKey=9d85a62254ac4052b9ff54e5d8425688"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch recipe details. Status code: {response.status_code}")
        return None

# Function to fetch ingredient price based on ingredient ID
def get_ingredient_price(ingredient_id):
    url = f"https://api.spoonacular.com/food/ingredients/{ingredient_id}/information?apiKey=9d85a62254ac4052b9ff54e5d8425688"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        ingredient_info = response.json()
        price = ingredient_info.get('estimatedCost', {}).get('value', None)
        if price is not None:
            return float(price)
        else:
            return None
    else:
        print(f"Failed to fetch ingredient price. Status code: {response.status_code}")
        return None

# Function to save a recipe to a JSON file
def save_recipe(recipe):
    if not os.path.exists(SAVED_RECIPES_FILE):
        with open(SAVED_RECIPES_FILE, 'w') as file:
            json.dump([], file)  # Initialize with an empty list if file doesn't exist
    
    with open(SAVED_RECIPES_FILE, 'r+') as file:
        recipes = json.load(file)
        recipes.append(recipe)
        file.seek(0)
        json.dump(recipes, file, indent=4)
    
    print(f"Recipe '{recipe['title']}' has been saved.")

# Function to display previously saved recipes
def display_saved_recipes():
    if os.path.exists(SAVED_RECIPES_FILE):
        with open(SAVED_RECIPES_FILE, 'r') as file:
            saved_recipes = json.load(file)
            if saved_recipes:
                print("\nPreviously saved recipes:")
                for idx, recipe in enumerate(saved_recipes, start=1):
                    print(f"{idx}. {recipe['title']} - {recipe['link']}")
            else:
                print("No recipes saved yet.")
    else:
        print("No saved recipes found.")

# Function to display the recipe information
def display_recipes(recipes, show_missing_ingredients, show_nutrition, show_instructions, show_prices):
    if recipes:
        for recipe in recipes:
            print(f"Recipe Title: {recipe['title']}")
            print(f"Used Ingredients: {[ingredient['name'] for ingredient in recipe['usedIngredients']]}")
            
            if show_missing_ingredients:
                missing_ingredients = recipe['missedIngredients']
                print(f"Missing Ingredients: {[ingredient['name'] for ingredient in missing_ingredients]}")
                
                if show_prices:
                    print("Prices for Missing Ingredients:")
                    for ingredient in missing_ingredients:
                        ingredient_price = get_ingredient_price(ingredient['id'])
                        if ingredient_price is not None:
                            print(f"Ingredient: {ingredient['name']} - Estimated Price: ${ingredient_price / 100:.2f}")
                        else:
                            print(f"Ingredient: {ingredient['name']} - Price not available")
            
            if show_instructions:
                instructions = get_recipe_instructions(recipe['id'])
                print(f"Instructions: {instructions}")
            
            if show_nutrition:
                recipe_details = get_recipe_details(recipe['id'])
                if recipe_details:
                    display_nutrition(recipe_details['nutrition'])

            print(f"Recipe Link: https://spoonacular.com/recipes/{recipe['id']}")
            print('-' * 40)
            
            # Ask the user if they want to save the recipe
            save_option = input(f"Do you want to save the recipe '{recipe['title']}'? (yes/no): ").strip().lower()
            if save_option == 'yes':
                # Save recipe details
                recipe_to_save = {
                    'title': recipe['title'],
                    'link': f"https://spoonacular.com/recipes/{recipe['id']}",
                    'used_ingredients': [ingredient['name'] for ingredient in recipe['usedIngredients']],
                    'missing_ingredients': [ingredient['name'] for ingredient in recipe['missedIngredients']]
                }
                save_recipe(recipe_to_save)
    else:
        print("No recipes found.")

# Main program logic
if __name__ == "__main__":
    # Load previously entered ingredients from the file
    previous_ingredients = load_ingredients_from_file()
    
    # Display the previous ingredients
    if previous_ingredients:
        print("Previously entered ingredients:")
        for ingredients in previous_ingredients:
            print(ingredients)
    
    # Prompt the user for ingredients (comma-separated)
    user_ingredients = input("Enter ingredients (comma-separated): ").strip().split(", ")
    
    # Add new ingredients to the file
    add_ingredients_to_list(user_ingredients)
    
    # Ask the user if they want to see missing ingredients
    show_missing_ingredients = input("Would you like to see missing ingredients with available recipes? (yes/no): ").strip().lower() == 'yes'
    
    # Ask the user if they want to see recipe instructions
    show_instructions = input("Would you like to see recipe instructions? (yes/no): ").strip().lower() == 'yes'
    
    # Ask the user if they want to see the nutrition facts
    show_nutrition = input("Would you like to see nutrition facts for each recipe? (yes/no): ").strip().lower() == 'yes'
    
    # Ask the user if they want to see ingredient prices (for missing ingredients only)
    show_prices = input("Would you like to see estimated prices for the missing ingredients? (yes/no): ").strip().lower() == 'yes'
    
    # Fetch the recipes based on the provided ingredients
    recipes = get_recipes(", ".join(user_ingredients))
    
    # Display the fetched recipes with or without missing ingredients, instructions, nutrition facts, and ingredient prices for missing ingredients based on user choice
    display_recipes(recipes, show_missing_ingredients, show_nutrition, show_instructions, show_prices)
    
    # Ask if the user wants to display previously saved recipes
    display_saved_option = input("Would you like to see your saved recipes? (yes/no): ").strip().lower()
    if display_saved_option == 'yes':
        display_saved_recipes()
