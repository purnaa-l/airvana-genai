import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import base64

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
st.set_page_config(page_title="PolluScan: Smart Pollution Analyzer", layout="centered", page_icon="🌱")

background_color = "#f5f7fa"  # Light background
text_color = "#ffffff"  # Dark text
card_background = ""  # Card background
button_color = "#4CAF50"  # Green button color


page_bg_img = """
<style>
/* Background */
[data-testid="stAppViewContainer"] {
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    background-image: url('https://images.unsplash.com/photo-1509515837298-2c67a3933321?q=80&w=3088&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');}

/* Transparent header and sidebar */
[data-testid="stHeader"], [data-testid="stSidebar"] {
    background: rgba(0,0,0,0);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown(f"""
<style>
    body {{
        background-color: {background_color};
        font-family: 'Segoe UI', sans-serif;
        color: {text_color};
    }}
    .stButton > button {{
        background-color: {button_color};
        color: white;
        padding: 12px 26px;
        border: none;
        border-radius: 10px;
        font-size: 18px;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
        transition: 0.3s;
        align-items: center;
    }}
    .stButton > button:hover {{
        background-color: #388E3C;
        transform: translateY(-3px);
        animation: pulse 1s infinite;
        align-items: center;
        justify-content: center;
        display: flex;
        text-align: center;
        font-size: 20px;
        font-weight: 700;
        text-decoration: none;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .stButton > button {{
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    .markdown-text-container {{
        background: {card_background};
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        text-color: black;
    }}
    .stImage > img {{
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
    }}
    h1, h2, h3 {{
        text-align: center;
        color: {text_color};
    }}
</style>
""", unsafe_allow_html=True)

st.title("🌱 PolluScan: Pollution Detection & Smart Recommendations")
st.markdown("<p style='text-align: center; color: #000000;'>Click a picture of the air around you, and get the smartest AI insights NOW!</p>", unsafe_allow_html=True)
#st.markdown(f"""
# <div class="markdown-text-container">
#     <h3>🔍 What PolluScan Offers:</h3>
#     <ul>
#         <li><b>Pollution Type Detection</b> from environment images (Air, Water, Land, Mixed)</li>
#         <li><b>Pollution Severity Analysis</b> (Low, Moderate, High, Hazardous)</li>
#         <li><b>Specific Observations</b> about the pollution</li>
#         <li><b>Personalized Actionable Recommendations</b> for Individuals & Communities</li>
#         <li><b>Multilingual Support</b> (Select your preferred language!)</li>
#     </ul>
#     <p>Ready to contribute to a cleaner planet? 🌍 Upload your photo now!</p>
# </div>
#""", unsafe_allow_html=True)

lang = st.selectbox("🌐 Choose your language for the report:", ["Kannada", "English", "Hindi", "Tamil", "Telugu"])
uploaded_file = st.file_uploader("📸 Upload a photo of the environment:", type=["jpeg", "jpg", "png"])
def get_gemini_response(input_prompt, image_parts):
    model = genai.GenerativeModel("gemini-2.5-flash") #model changed to "gemini-2.5-flash" from 1.5-pro due to token limit issues
    response = model.generate_content([input_prompt, image_parts[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No image uploaded!")
prompt_template = f"""
You are an experienced environmental scientist and public health expert.

Analyze the uploaded photo of the air quality around the user and provide a comprehensive, actionable report, structured as follows:

Current Air Quality Condition:

Describe how the air around the user appears (e.g., hazy, clear, polluted, etc.).

Mention any visible pollution signs such as smog, smoke, dust, or chemical fumes.

Pollution Type:

Identify the type(s) of pollution present (e.g., air pollution, industrial emissions, wildfire smoke, etc.).

Pollution Severity:

Provide a Pollution Severity Level:

Low

Moderate

High

Hazardous

Mention the environmental or health risks associated with the identified severity level.

Specific Observations:

Highlight any visible environmental damage (e.g., hazy sky, polluted water bodies, damaged vegetation).

Assess how the current pollution may affect the immediate surroundings (e.g., local ecosystems, nearby communities).

Personalized Recommendations:

Suggest immediate actions the user can take to reduce exposure to the pollution.

Provide long-term strategies for improving air quality in the area (e.g., use of air purifiers, reducing car emissions, planting trees).

Tailor your recommendations based on the severity and type of pollution.

Additional Insights:

If possible, suggest how the weather, local geography, or seasonality might be influencing the pollution levels.

Offer specific tips based on the user's location (if available) to improve their environment (e.g., air quality apps, local policies).

**Output the full report in {lang} language**.

Structure the output with:
- Bold headings
- Clear bullet points
- Easy readability
"""
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 Uploaded Environment Image", use_column_width=True)

    if st.button("🔍 Analyze Pollution"):
        try:
            with st.spinner('♻️ Analyzing Environment... Hold on! 🌿'):
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(prompt_template, image_data)

            st.success("Analysis Complete! 🌟")
            st.markdown(f"""
                <div class="leaves-animation">
                    <div class="leaf" style="top: 10%; left: 20%;"></div>
                    <div class="leaf" style="top: 30%; left: 40%;"></div>
                    <div class="leaf" style="top: 50%; left: 60%;"></div>
                    <div class="leaf" style="top: 70%; left: 80%;"></div>
                </div>
            """, unsafe_allow_html=True)

            st.header("🌿 Pollution Analysis Report")
            st.markdown(response, unsafe_allow_html=True)

            report_bytes = response.encode('utf-8')
            st.download_button(
                label="📥 Download Pollution Report",
                data=report_bytes,
                file_name=f"pollution_report_{lang.lower()}.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Error analyzing the image: {e}")
