import streamlit as st
from alternative import get_recipes, display_recipes  # Import your functions

# Set the page configuration
st.set_page_config(page_title="Recipe Finder", layout="wide")

# Initialize session state for ingredients if it doesn't exist
if 'ingredients' not in st.session_state:
    st.session_state['ingredients'] = []
if 'ingredient_input' not in st.session_state:
    st.session_state['ingredient_input'] = ""

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
st.header("Fetch Recipes")
if st.button("FETCH RECIPES"):
    if st.session_state['ingredients']:
        user_ingredients = ", ".join(st.session_state['ingredients'])
        
        # Fetch the recipes based on the provided ingredients
        recipes = get_recipes(user_ingredients)

        # Check if recipes is None and handle the error
        if recipes is None:
            st.error("Error fetching recipes. Please try again.")
        else:
            # Display the fetched recipes
            st.subheader("Recipes Found:")
            display_recipes(recipes)

            # Display the recipe results
            for recipe in recipes:  # Assuming 'recipes' is a list of recipe names or details
                st.write(recipe)  # Display each recipe
    else:
        st.warning("Please add at least one ingredient to fetch recipes.")

show_missing_ingredients = st.checkbox("Show Missing Ingredients", value=True)
show_instructions = st.checkbox("Show Instructions", value=True)
show_nutrition = st.checkbox("Show Nutrition Facts", value=True)
show_prices = st.checkbox("Show Prices", value=True)