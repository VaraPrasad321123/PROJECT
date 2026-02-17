import streamlit as st
import os
from google import genai
from PIL import Image
from dotenv import load_dotenv

# -----------------------------------
# Load Environment Variables
# -----------------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Missing GOOGLE_API_KEY. Please check your .env file.")
    st.stop()

# Create Gemini Client
client = genai.Client(api_key=api_key)

# -----------------------------------
# Get Available Models
# -----------------------------------
# -----------------------------------
# Get Available Models (NEW SDK SAFE)
# -----------------------------------
available_models = []

try:
    models = client.models.list()
    for m in models:
        # Only include Gemini models
        if "gemini" in m.name.lower():
            available_models.append(m.name)

except Exception as e:
    st.sidebar.error(f"Error listing models: {e}")

# -----------------------------------
# Sidebar Configuration
# -----------------------------------
st.sidebar.header("⚙️ Configuration")

selected_model_name = st.sidebar.selectbox(
    "Select Model",
    available_models,
    index=0 if available_models else None
)

# -----------------------------------
# Gemini Response Function
# -----------------------------------
def get_gemini_response(user_text, uploaded_file, system_prompt, model_name):
    try:
        image = Image.open(uploaded_file)

        response = client.models.generate_content(
            model=model_name,
            contents=[
                system_prompt,
                image,
                user_text if user_text else "Provide full structural analysis."
            ]
        )

        return response.text

    except Exception as e:
        return f"Error: {e}"

# -----------------------------------
# Streamlit UI
# -----------------------------------
st.set_page_config(
    page_title="Civil Engineering Insight Studio",
    layout="centered"
)

st.header("🏗️ Civil Engineering Insight Studio")
st.write("Upload a structure image for professional engineering analysis.")

# User Input
input_text = st.text_input(
    "Additional Context (Optional):",
    placeholder="e.g., focus on structural integrity or load distribution"
)

uploaded_file = st.file_uploader(
    "Upload Structure Image",
    type=["jpg", "jpeg", "png"]
)

# Show Uploaded Image
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Target Structure", use_container_width=True)

analyze_button = st.button("Analyze Structure")

# Engineering Prompt
system_prompt = """
You are an expert civil engineer.

Analyze the uploaded structure image and provide a professional engineering report including:

1. Type of structure
2. Materials likely used
3. Estimated dimensions
4. Construction techniques
5. Structural integrity observations
6. Possible engineering challenges
7. Safety recommendations

Be technical, structured, and professional.
"""

# -----------------------------------
# Run Analysis
# -----------------------------------
if analyze_button:
    if uploaded_file is not None:
        if not selected_model_name:
            st.error("No model available for selection.")
        else:
            with st.spinner("Analyzing structural data..."):
                result = get_gemini_response(
                    input_text,
                    uploaded_file,
                    system_prompt,
                    selected_model_name
                )

            st.subheader("📋 Engineering Report")
            st.write(result)

    else:
        st.warning("Please upload an image before analysis.")
