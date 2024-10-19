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

# Show checkboxes for additional options
show_missing_ingredients = st.checkbox("Show Missing Ingredients", value=True)
show_instructions = st.checkbox("Show Instructions", value=True)
show_nutrition = st.checkbox("Show Nutrition Facts", value=True)
show_prices = st.checkbox("Show Prices", value=True)

# Add a square section in the middle of the page
# You can include this again or remove it as needed
st.markdown("<div style='display: flex; justify-content: center;'><div style='width: 60vh; height: 60vh; border: 1px solid white; display: flex; align-items: center; justify-content: center;'>"
            "<h3>This is the middle square section</h3></div></div>", unsafe_allow_html=True)

