import requests

# Your Spoonacular API key (replace with your actual API key)
API_KEY = "your_spoonacular_api_key"

# Function to fetch recipes based on ingredients
def get_recipes(ingredients):
    # Construct the API URL with the provided ingredients
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=5&apiKey={API_KEY}"
    
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

# Function to display the recipe information
def display_recipes(recipes):
    if recipes:
        # Iterate through each recipe and display its information
        for recipe in recipes:
            print(f"Recipe Title: {recipe['title']}")
            print(f"Used Ingredients: {[ingredient['name'] for ingredient in recipe['usedIngredients']]}")
            print(f"Missing Ingredients: {[ingredient['name'] for ingredient in recipe['missedIngredients']]}")
            print(f"Recipe Link: https://spoonacular.com/recipes/{recipe['id']}")
            print('-' * 40)
    else:
        print("No recipes found.")

# Main program logic
if __name__ == "__main__":
    # Prompt the user for ingredients (comma-separated)
    user_ingredients = input("Enter ingredients (comma-separated): ").strip()
    
    # Fetch the recipes based on the provided ingredients
    recipes = get_recipes(user_ingredients)
    
    # Display the fetched recipes
    display_recipes(recipes)
