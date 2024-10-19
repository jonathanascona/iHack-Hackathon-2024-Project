# HACKATHON FALL SEMESTER 2024 #
# DYLAN KOHN, JONATHAN NELSON, JONATHAN ASCONA #
# 10/18/24 - 10/19/24)


import requests

# Your Spoonacular API key
API_KEY = "9d85a62254ac4052b9ff54e5d8425688"

# Function to fetch recipes based on ingredients
def get_recipes(ingredients):
    # Construct the API URL with the provided ingredients and your API key
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=5&apiKey=9d85a62254ac4052b9ff54e5d8425688"
    
    # Make the request to Spoonacular
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Return the JSON response containing the recipes
        return response.json()
    else:
        # If something went wrong, print the status and return None
        print(f"Failed to fetch recipes. Status code: {response.status_code}")
        return None

# Function to fetch detailed recipe information including instructions and nutrition facts
def get_recipe_details(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?includeNutrition=true&apiKey={API_KEY}"
    
    # Make the request to Spoonacular
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch recipe details. Status code: {response.status_code}")
        return None

# Function to fetch ingredient price based on ingredient ID
def get_ingredient_price(ingredient_id):
    url = f"https://api.spoonacular.com/food/ingredients/{ingredient_id}/information?apiKey={API_KEY}"
    
    # Make the request to Spoonacular
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        ingredient_info = response.json()
        price = ingredient_info.get('estimatedCost', {}).get('value', None)
        if price is not None:
            return float(price)  # Convert to float for consistency
        else:
            return None  # No price available
    else:
        print(f"Failed to fetch ingredient price. Status code: {response.status_code}")
        return None

# Function to display nutrition facts in a Nutrition Facts Chart style
def display_nutrition(nutrition):
    if nutrition:
        nutrients = nutrition['nutrients']
        print("Nutrition Facts".center(40, " "))
        print("=" * 40)
        print(f"{'Amount per serving'.ljust(30)}")
        print("=" * 40)
        for nutrient in nutrients:
            if nutrient['name'] in ["Calories", "Fat", "Carbohydrates", "Protein", "Fiber", "Sodium", "Sugar"]:
                print(f"{nutrient['name'].ljust(25)}{str(nutrient['amount']).rjust(10)} {nutrient['unit']}")
        print("=" * 40)
    else:
        print("No nutrition information available.")

# Function to display recipe instructions
def get_recipe_instructions(recipe_id):
    recipe_details = get_recipe_details(recipe_id)
    if recipe_details:
        return recipe_details.get('instructions', "No instructions available.")
    else:
        return "No instructions available."

# Function to display the recipe information
def display_recipes(recipes, show_missing_ingredients, show_nutrition, show_instructions, show_prices):
    if recipes:
        # Iterate through each recipe and display its information
        for recipe in recipes:
            print(f"Recipe Title: {recipe['title']}")
            print(f"Used Ingredients: {[ingredient['name'] for ingredient in recipe['usedIngredients']]}")
            
            # Option to show or hide missing ingredients based on user input
            if show_missing_ingredients:
                missing_ingredients = recipe['missedIngredients']
                print(f"Missing Ingredients: {[ingredient['name'] for ingredient in missing_ingredients]}")
                
                # If the user chose to see prices, fetch prices for the missing ingredients
                if show_prices:
                    print("Prices for Missing Ingredients:")
                    for ingredient in missing_ingredients:
                        ingredient_price = get_ingredient_price(ingredient['id'])
                        if ingredient_price is not None:
                            print(f"Ingredient: {ingredient['name']} - Estimated Price: ${ingredient_price / 100:.2f}")
                        else:
                            print(f"Ingredient: {ingredient['name']} - Price not available")

            # Fetch and display recipe instructions if user chose to see them
            if show_instructions:
                instructions = get_recipe_instructions(recipe['id'])
                print(f"Instructions: {instructions}")
            
            print(f"Recipe Link: https://spoonacular.com/recipes/{recipe['id']}")
            
            # Fetch and display nutrition facts if user chose to see them
            if show_nutrition:
                recipe_details = get_recipe_details(recipe['id'])
                if recipe_details and 'nutrition' in recipe_details:
                    display_nutrition(recipe_details['nutrition'])

            print('-' * 40)
    else:
        print("No recipes found.")

# Main program logic
if __name__ == "__main__":
    # Prompt the user for ingredients (comma-separated)
    user_ingredients = input("Enter ingredients (comma-separated): ").strip()
    
    # Ask the user if they want to see the missing ingredients
    show_missing_ingredients = input("Would you like to see missing ingredients with available recipes? (yes/no): ").strip().lower() == 'yes'
    
    # Ask the user if they want to see recipe instructions
    show_instructions = input("Would you like to see recipe instructions? (yes/no): ").strip().lower() == 'yes'
    
    # Ask the user if they want to see the nutrition facts
    show_nutrition = input("Would you like to see nutrition facts for each recipe? (yes/no): ").strip().lower() == 'yes'
    
    # Ask the user if they want to see ingredient prices (for missing ingredients only)
    show_prices = input("Would you like to see estimated prices for the missing ingredients? (yes/no): ").strip().lower() == 'yes'
    
    # Fetch the recipes based on the provided ingredients
    recipes = get_recipes(user_ingredients)
    
    # Display the fetched recipes with or without missing ingredients, instructions, nutrition facts, and ingredient prices for missing ingredients based on user choice
    display_recipes(recipes, show_missing_ingredients, show_nutrition, show_instructions, show_prices)

