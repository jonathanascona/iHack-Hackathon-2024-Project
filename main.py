import streamlit as st
import pandas as pd
from alternative import get_recipe, display_recipes, get_recipe_details  # Import your functions

# Set the page configuration
st.set_page_config(page_title="Recipe Finder", layout="wide")

# Initialize session state for ingredients if it doesn't exist
if 'ingredients' not in st.session_state:
    st.session_state['ingredients'] = []
if 'ingredient_input' not in st.session_state:
    st.session_state['ingredient_input'] = ""
if 'ingredient_amount' not in st.session_state:
    st.session_state['ingredient_amount'] = ""
if 'input_cleared' not in st.session_state:
    st.session_state['input_cleared'] = False  # Flag to manage input clearing

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

# Function to add an ingredient and reset input indirectly
def add_ingredient():
    if st.session_state['ingredient_input']:  # Only add if the input is not empty
        ingredient = st.session_state['ingredient_input']
        amount = st.session_state['ingredient_amount']
        
        # Add both ingredient and amount (if provided) to the ingredients list
        if amount:
            st.session_state['ingredients'].append(f"{ingredient} ({amount})")
        else:
            st.session_state['ingredients'].append(ingredient)
        
        # Clear inputs by using st.session_state.update() without directly modifying widget state
        st.session_state.update({
            'ingredient_input': "",  # Reset ingredient input safely
            'ingredient_amount': ""  # Reset amount input safely
        })

# Function to clear all ingredients
def clear_ingredients():
    st.session_state['ingredients'] = []  # Reset the ingredients list

# Sidebar on the right
with st.sidebar:
    st.header("Saved Recipes")
    with st.expander("View Saved Recipes"):
        # Button to export saved recipes to a CSV file
        if st.button("Export to CSV"):
            csv = convert_to_csv(saved_recipes)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name='saved_recipes.csv',
                mime='text/csv'
            )

    # Button to clear all ingredients
    if st.button("Clear All Ingredients"):
        clear_ingredients()

    # Display the list of ingredients
    st.header("Current Ingredients")
    if st.session_state['ingredients']:
        st.markdown("\n".join(f"- {ingredient}" for ingredient in st.session_state['ingredients']))
    else:
        st.write("No ingredients added.")

# Main section for input and recipe fetching
st.header("Quick Bite")

# Two columns: one for ingredient and one for amount
ingredient_col, amount_col = st.columns([2, 1])

with ingredient_col:
    st.text_input(
        "Enter your ingredient",
        placeholder="e.g. chicken, rice",
        key='ingredient_input'
    )

with amount_col:
    st.text_input(
        "Amount (optional)",
        placeholder="e.g. 200g, 2 cups",
        key='ingredient_amount'
    )

# Two columns for the add ingredient and fetch recipes buttons
col1, col2 = st.columns([1, 1])

# Add Ingredients button in the left column
with col1:
    if st.button("Add Ingredients"):
        add_ingredient()  # Call the add_ingredient function when the button is pressed

# Fetch Recipes button in the right column
with col2:
    if st.button("FETCH RECIPES"):
        if st.session_state['ingredients']:
            user_ingredients = ", ".join(st.session_state['ingredients'])
            st.header("Recipes Based on Your Ingredients")

            # Fetch the recipes based on the provided ingredients
            recipes = get_recipe(user_ingredients)

            # Check if recipes is None and handle the error
            if recipes is None:
                st.error("Error fetching recipes. Please try again.")
            else:
                st.subheader("Recipes Found:")

                # Display the recipe results inside the square container
                for recipe in recipes:  # Assuming 'recipes' is a list of recipe details
                    st.markdown(f"<div style='margin: 5px; text-align: left;'><strong>{recipe['title']}</strong></div>", unsafe_allow_html=True)

                    # Fetch and display detailed recipe information
                    recipe_details = get_recipe_details(recipe['id'])  # Fetch detailed recipe information
                    if recipe_details:
                        # Display cooking instructions
                        instructions = recipe_details.get('instructions', 'No instructions available.')
                        st.markdown(f"<p><strong>Instructions:</strong> {instructions}</p>", unsafe_allow_html=True)

                        # Display used and missing ingredients
                        used_ingredients = [ingredient['name'] for ingredient in recipe_details['usedIngredients']]
                        st.markdown(f"<p><strong>Used Ingredients:</strong> {', '.join(used_ingredients)}</p>", unsafe_allow_html=True)

                        missing_ingredients = [ingredient['name'] for ingredient in recipe_details['missedIngredients']]
                        st.markdown(f"<p><strong>Missing Ingredients:</strong> {', '.join(missing_ingredients)}</p>", unsafe_allow_html=True)

                        # Display nutrition facts if available
                        nutrition = recipe_details.get('nutrition')
                        if nutrition:
                            nutrients = nutrition['nutrients']
                            nutrition_info = "\n".join(f"{nutrient['name']}: {nutrient['amount']} {nutrient['unit']}" for nutrient in nutrients)
                            st.markdown(f"<p><strong>Nutrition Facts:</strong><br>{nutrition_info}</p>", unsafe_allow_html=True)

                        # Link to the recipe
                        st.markdown(f"[View Full Recipe](https://spoonacular.com/recipes/{recipe['id']})", unsafe_allow_html=True)
        else:
            st.warning("Please add at least one ingredient to fetch recipes.")

# Additional features section
with st.expander("Show Additional Features"):
    show_missing_ingredients = st.checkbox("Show Missing Ingredients", value=True)
    show_instructions = st.checkbox("Show Instructions", value=True)
    show_nutrition = st.checkbox("Show Nutrition Facts", value=True)
    show_prices = st.checkbox("Show Prices", value=True)
    show_missing_item_prices = st.checkbox("Show Missing Item Prices", value=True)

# Footer with background image using base64 encoding
import base64

# Function to convert local image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as file:
        data = file.read()
    return base64.b64encode(data).decode()

# Local path to the image
image_path = "C:\\Users\\jonat\\Documents\\GitHub\\ihackf24-main\\background_wallpaper.jpg"
base64_image = get_base64_image(image_path)

# Footer with background image using base64 encoding
footer_html = f"""
    <style>
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-image: url("data:image/jpg;base64,{base64_image}");
        background-size: cover;
        background-repeat: no-repeat;
        padding: 30px;
        text-align: center;
        color: white;
        font-size: 16px;
    }}
    </style>
    <div class="footer">
   
    </div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
