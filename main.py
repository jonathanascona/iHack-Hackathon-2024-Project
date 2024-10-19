import streamlit as st
import pandas as pd
from PIL import Image
import requests
import io
import base64

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
if 'show_uploader' not in st.session_state:
    st.session_state['show_uploader'] = False  # Flag to toggle uploader visibility

# Spoonacular API Key (replace 'your_api_key' with your actual API key)
spoonacular_api_key = "your_api_key"

# Function to add an ingredient and reset input
def add_ingredient():
    if st.session_state['ingredient_input']:  # Only add if the input is not empty
        ingredient = st.session_state['ingredient_input']
        amount = st.session_state['ingredient_amount']
        
        # Add both ingredient and amount (if provided) to the ingredients list
        if amount:
            st.session_state['ingredients'].append(f"{ingredient} ({amount})")
        else:
            st.session_state['ingredients'].append(ingredient)
        
        # Clear inputs safely
        st.session_state.update({
            'ingredient_input': "",  # Reset ingredient input
            'ingredient_amount': ""  # Reset amount input
        })

# Function to clear all ingredients
def clear_ingredients():
    st.session_state['ingredients'] = []  # Reset the ingredients list

# Function to detect the ingredient from an uploaded image using Spoonacular API
def detect_ingredient(image):
    api_url = f"https://api.spoonacular.com/food/images/analyze?apiKey={spoonacular_api_key}"
    response = requests.post(api_url, files={"file": image})
    
    if response.status_code == 200:
        # Assuming the API returns 'category' or similar as the detected ingredient
        return response.json().get("category", "Unknown ingredient")
    return "Error detecting ingredient"

# Sidebar on the right
with st.sidebar:
    st.header("Saved Recipes")
    with st.expander("View Saved Recipes"):
        # Button to export saved recipes to a CSV file
        if st.button("Export to CSV"):
            csv = pd.DataFrame(st.session_state['ingredients']).to_csv(index=False)
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
st.header("QUICKBITE")

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

# Two columns for the add ingredient and upload photo buttons
col1, col2 = st.columns([1, 1])

# Add Ingredients button in the left column
with col1:
    if st.button("Add Ingredients"):
        add_ingredient()  # Call the add_ingredient function when the button is pressed

# Upload Photo button in the right column (Same size as Add Ingredients)
with col2:
    if st.button("Upload Photo"):
        st.session_state['show_uploader'] = True  # Show the file uploader when the button is clicked

# Display file uploader and process the image without showing it
if st.session_state['show_uploader']:
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    if uploaded_image:
        # Convert the image to bytes and detect the ingredient without displaying it
        img_bytes = io.BytesIO()
        image = Image.open(uploaded_image)
        image.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        # Call the backend API or detection function
        detected_ingredient = detect_ingredient(img_bytes)
        st.write(f"Detected Ingredient: **{detected_ingredient}**")

        # Optional: Allow the user to add the detected ingredient
        if st.button("Add Detected Ingredient"):
            st.session_state['ingredients'].append(detected_ingredient)

# Fetch Recipes button
if st.button("FETCH RECIPES"):
    if st.session_state['ingredients']:
        user_ingredients = ", ".join(st.session_state['ingredients'])
        st.header("Recipes Based on Your Ingredients")

        # Simulating fetching recipes based on the ingredients
        recipes = get_recipe(user_ingredients)  # Use actual API in production

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

