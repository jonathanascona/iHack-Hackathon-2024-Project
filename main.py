import streamlit as st
import pandas as pd 
from alternative import get_recipes, display_recipes  # Import your functions

# Set the page configuration
st.set_page_config(page_title="Recipe Finder", layout="wide")

# Initialize session state for ingredients if it doesn't exist
if 'ingredients' not in st.session_state:
    st.session_state['ingredients'] = []
if 'ingredient_input' not in st.session_state:
    st.session_state['ingredient_input'] = ""

# Sample saved recipes list (you can replace this with actual recipe data)
saved_recipes = [
    {"Recipe Name": "Spaghetti Bolognese", "Ingredients": "Pasta, Beef, Tomato Sauce", "Cooking Time": "30 min"},
    {"Recipe Name": "Chicken Curry", "Ingredients": "Chicken, Curry Paste, Coconut Milk", "Cooking Time": "45 min"},
    {"Recipe Name": "Pancakes", "Ingredients": "Flour, Eggs, Milk", "Cooking Time": "15 min"}
]

# Function to convert the saved recipes into a CSV format
def convert_to_csv(data):
    df = pd.DataFrame(data)  # Convert list of recipes into a DataFrame
    return df.to_csv(index=False)

# Sidebar on the right
with st.sidebar:
    st.header("Saved Recipes")  # Sidebar header

    # Button to export saved recipes to a CSV file
    if st.button("Export to CSV"):
        csv = convert_to_csv(saved_recipes)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name='saved_recipes.csv',
            mime='text/csv'
        )

def clear_ingredients():
    st.session_state['ingredients'] = []  # Reset the ingredients list

# Sidebar for ingredient input
st.sidebar.header("Add Ingredients")

if st.sidebar.button("Clear All Ingredients"):
    clear_ingredients()

# Function to add ingredient and reset input
def add_ingredient():
    if st.session_state['ingredient_input']:  # Only add if the input is not empty
        st.session_state['ingredients'].append(st.session_state['ingredient_input'])  # Add to the ingredients list
        st.session_state['ingredient_input'] = ""  # Clear the input field

# Text input for ingredients, tied to session state and using on_change callback
st.sidebar.text_input(
    "Enter your ingredient",
    placeholder="e.g. chicken, rice",
    key='ingredient_input',
    on_change=add_ingredient  # This will be triggered when input changes or the "Enter" key is pressed
)

# Display the list of ingredients
st.sidebar.header("Current Ingredients")
if st.session_state['ingredients']:
    # Display each ingredient on a new line using markdown
    st.sidebar.markdown("\n".join(f"- {ingredient}" for ingredient in st.session_state['ingredients']))
else:
    st.sidebar.write("No ingredients added.")

# Fetching recipes section
st.header("Quick Bite")
if st.button("FETCH RECIPES"):
    if st.session_state['ingredients']:
        user_ingredients = ", ".join(st.session_state['ingredients'])
        
        # Fetch the recipes based on the provided ingredients
        recipes = get_recipes(user_ingredients)

        # Check if recipes is None and handle the error
        if recipes is None:
            st.error("Error fetching recipes. Please try again.")
        else:
            # Display the fetched recipes inside the square section
            st.subheader("Recipes Found:")
            # Create the square container
            recipe_container = st.markdown("<div style='display: flex; justify-content: center;'><div style='width: 40vh; height: 40vh; border: 1px solid white; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; padding: 10px;'>"
                                            "<h4>Recipes:</h4></div></div>", unsafe_allow_html=True)

            # Display the recipe results inside the square container
            for recipe in recipes:  # Assuming 'recipes' is a list of recipe names or details
                st.markdown(f"<div style='margin: 5px; text-align: center;'><strong>{recipe['title']}</strong></div>", unsafe_allow_html=True)  # Display each recipe
            
            # Optionally, you could also include more detailed recipe information here

    else:
        st.warning("Please add at least one ingredient to fetch recipes.")

with st.expander("Show Additional Features"):
    show_missing_ingredients = st.checkbox("Show Missing Ingredients", value=True)
    show_instructions = st.checkbox("Show Instructions", value=True)
    show_nutrition = st.checkbox("Show Nutrition Facts", value=True)
    show_prices = st.checkbox("Show Prices", value=True)
    show_missing_item_prices = st.checkbox("Show Missing Item Prices", value=True)
>>>>>>> c3621f6c56cba035be6be6c910308f6ceff9e428
