import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
st.set_page_config(
    page_title="HealthifyAI - Breathe Better, Live Stronger",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)
pg_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
[data-testid="stHeader"], [data-testid="stSidebar"] {
    background: rgba(0, 0, 0, 0);
}
</style>
"""
st.markdown(pg_bg_img, unsafe_allow_html=True)
st.markdown("""
<style>
html, body, [class*="css"] {
    color: black;
    font-family: 'Poppins', sans-serif;
    text-align: center;
}

h1, h2, h3, h4, h5, h6 {
    text-align: center;
}

.healthify-card {
    background: rgba(255, 255, 255, 0.8);
    border-radius: 20px;
    padding: 2rem;
    backdrop-filter: blur(15px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    margin-top: 30px;
    color: black;
}

.more-tips-button {
    background-color: #00bfa5;
    color: white;
    padding: 12px 24px;
    border-radius: 12px;
    border: none;
    font-weight: bold;
    margin-top: 25px;
    cursor: pointer;
    font-size: 1.1rem;
}

.tagline {
    font-size: 1.4rem;
    color: #00796b;
    margin-bottom: 30px;
}

.aqi-link {
    font-size: 1rem;
    color: #00796b;
    text-decoration: none;
    font-weight: bold;
}
.aqi-link:hover {
    color: #004d40;
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")

def get_health_advice(user_query, current_aqi, user_health_conditions=[]):
    prompt = f"""
    You are HealthifyAI, a highly professional health assistant specialized in air quality and health.

    Current AQI: {current_aqi}
    User Health Conditions: {', '.join(user_health_conditions) if user_health_conditions else "None"}

    Instructions:
    - Summarize impact of AQI briefly (max 3 lines).
    - List 2-3 personalized actionable steps.
    - Provide a Risk Level (Low/Moderate/High/Severe).
    - Recommend emergency contacts or steps if Risk Level is High or Severe.
    - Make it very clear, professional, friendly and reassuring.

    User Query:
    \"{user_query}\"
    """
    response = model.generate_content(prompt)
    return response.text.strip()

def save_to_csv(user_query, current_aqi, user_health_conditions, advice_text):
    now = datetime.now()
    data = {
        "Date": now.strftime("%Y-%m-%d"),
        "Time": now.strftime("%H:%M:%S"),
        "User Query": user_query,
        "AQI": current_aqi,
        "Health Conditions": ', '.join(user_health_conditions) if user_health_conditions else "None",
        "Advice": advice_text
    }
    df = pd.DataFrame([data])
    
    if not os.path.exists("healthifyai_advice.csv"):
        df.to_csv("healthifyai_advice.csv", index=False)
    else:
        df.to_csv("healthifyai_advice.csv", mode='a', header=False, index=False)

st.title("🌿🏥 HealthifyAI")
st.markdown("<div class='tagline'>Empowering Your Breath, Elevating Your Life. <br> Because Every Breath Matters.</div>", unsafe_allow_html=True)

with st.form("healthify_form"):
    user_query = st.text_input("💬 Ask HealthifyAI your health-related question:")
    current_aqi = st.slider("🌫️ Current AQI Level", min_value=0, max_value=500, value=100)
    
    st.markdown(
        "<a class='aqi-link' href='https://www.iqair.com/world-air-quality' target='_blank'>🌎 Don't know your AQI? Click here!</a>",
        unsafe_allow_html=True
    )
    
    user_conditions = st.text_input("🩺 Your Health Concerns (optional, comma separated):", placeholder="e.g., asthma, heart disease")
    
    submit = st.form_submit_button("Get Personalized Advice ✅")

if submit and user_query:
    with st.spinner('Analyzing air quality and your health profile...'):
        advice_text = get_health_advice(
            user_query=user_query,
            current_aqi=current_aqi,
            user_health_conditions=[c.strip() for c in user_conditions.split(",")] if user_conditions else []
        )
    
        save_to_csv(
        user_query=user_query,
        current_aqi=current_aqi,
        user_health_conditions=[c.strip() for c in user_conditions.split(",")] if user_conditions else [],
        advice_text=advice_text
    )
    st.markdown(f"<div class='healthify-card'>{advice_text}</div>", unsafe_allow_html=True)
    st.session_state.extra_tips = ""


# --- FOOTER ---
st.markdown("---")
st.caption("Crafted with ❤️ by HealthifyAI; AirVana's Best AI-Powered Health Bot • Because Every Breath Matters.")
