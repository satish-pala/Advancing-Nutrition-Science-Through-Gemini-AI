import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

# -------------------------
# Load API Key
# -------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("API Key not found. Check your .env file.")
    st.stop()

# -------------------------
# Initialize Gemini Client
# -------------------------
client = genai.Client(api_key=api_key)

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Nutrition AI", layout="centered")
st.title("🥗 NutritionAI - Instant Nutritional Information")

# -------------------------
# Nutrition Prompt Function
# -------------------------
def nutrition_prompt(food_item):
    return f"""
Provide detailed nutritional information for the following food item:

Food: {food_item}

Include:
- Calories
- Macronutrients (Protein, Fat, Carbohydrates)
- Micronutrients (Vitamins, Minerals)
- Health benefits
"""

# -------------------------
# User Input
# -------------------------
food_item = st.text_input("Enter food items (separate by commas):")

if st.button("Get Nutritional Information"):
    if food_item.strip() == "":
        st.warning("Please enter a food item.")
    else:
        with st.spinner("Analyzing nutrition..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=nutrition_prompt(food_item)
            )

        output_text = response.candidates[0].content.parts[0].text
        st.subheader("📊 Nutritional Information:")
        st.write(output_text)

