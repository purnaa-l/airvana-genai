import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai
import os

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Page Setup
st.set_page_config(page_title="🌱 EcoImpact Simulator", layout="wide")

# Background Styling
with st.container():
    st.markdown("""
        <style>
        .main {
            background-image: url('https://images.unsplash.com/photo-1558980664-10e7170e8d77');
            background-size: cover;
            background-position: center;
        }
        </style>
        """, unsafe_allow_html=True)

# Title & Intro
st.title("💚 EcoImpact: Sustainable Lifestyle Simulator")
st.markdown("""
    Discover how your everyday choices impact the 🌍 planet.  
    **EcoImpact** helps you visualize your carbon footprint and guides you toward greener, healthier habits.
""")

# Sidebar - User Inputs
st.sidebar.header("📥 Your Daily Choices")
travel_mode = st.sidebar.selectbox("🚗 Commute Mode", ["Gas Car", "Electric Car", "Bus", "Cycle", "Walk"])
distance_km = st.sidebar.slider("🛣️ Commute Distance (km)", 1, 50, 10)
home_energy = st.sidebar.selectbox("⚡ Home Energy Source", ["Coal", "Natural Gas", "Mixed Grid", "Solar", "Wind"])
diet_type = st.sidebar.radio("🍽️ Diet Type", ["Omnivore", "Mostly Vegetarian", "Vegan"])
aqi_input = st.sidebar.text_input("🌫️ AQI Level (optional)", "")
st.sidebar.markdown("[❓ Don’t know your AQI? Click here](https://www.iqair.com/world-air-quality)")

# Sidebar - Goal Setting
st.sidebar.header("🎯 Set Your Eco Goals")
daily_goal = st.sidebar.slider("🌱 Your Target CO₂ per Day (kg)", 0, 15, 5)

# Emission Calculations
emission_factors = {"Gas Car": 0.271, "Electric Car": 0.121, "Bus": 0.089, "Cycle": 0.0, "Walk": 0.0}
energy_emissions = {"Coal": 5.0, "Natural Gas": 3.5, "Mixed Grid": 2.5, "Solar": 0.2, "Wind": 0.1}
diet_emissions = {"Omnivore": 2.5, "Mostly Vegetarian": 1.7, "Vegan": 1.1}

travel_emission = distance_km * 2 * emission_factors[travel_mode]
home_emission = energy_emissions[home_energy]
food_emission = diet_emissions[diet_type]
total_emission = travel_emission + home_emission + food_emission

# Dynamic Feedback
st.sidebar.markdown("#### 🎉 Feedback")
if total_emission < daily_goal:
    st.sidebar.success(f"Awesome! You're emitting only {total_emission:.2f} kg – below your goal!")
else:
    st.sidebar.warning(f"Try to reduce from {total_emission:.2f} kg to your goal of {daily_goal} kg.")

# Main Dashboard
st.header("📊 Your EcoImpact Dashboard")
col1, col2 = st.columns(2)

with col1:
    st.metric("🌡️ Total Daily CO₂", f"{total_emission:.2f} kg", delta=f"Goal: {daily_goal} kg")
    st.metric("💓 Health Score", "Moderate" if travel_mode != "Walk" else "High")
    st.metric("🌿 Environmental Score", "Good" if home_energy in ["Solar", "Wind"] else "Needs Improvement")
    st.progress(min(100, int(total_emission * 2)))

with col2:
    fig, ax = plt.subplots()
    ax.bar(['Travel', 'Home', 'Diet'],
           [travel_emission, home_emission, food_emission],
           color=['#4CAF50', '#2196F3', '#FFC107'])
    ax.set_ylabel("kg CO₂")
    ax.set_title("Daily Emission Breakdown")
    st.pyplot(fig)

# More Graphs
with st.expander("📈 View All Data"):
    col1, col2, col3 = st.columns(3)
    with col1:
        fig1, ax1 = plt.subplots()
        ax1.bar(emission_factors.keys(), emission_factors.values())
        ax1.set_title("Commute Emissions (per km)")
        st.pyplot(fig1)
    with col2:
        fig2, ax2 = plt.subplots()
        ax2.bar(energy_emissions.keys(), energy_emissions.values(), color="orange")
        ax2.set_title("Energy Source Emissions")
        st.pyplot(fig2)
    with col3:
        fig3, ax3 = plt.subplots()
        ax3.bar(diet_emissions.keys(), diet_emissions.values(), color="green")
        ax3.set_title("Diet Emissions")
        st.pyplot(fig3)

# Formula Explanation
with st.expander("🎓 How We Calculate Impact"):
    st.markdown("""
    **Calculation Formula:**  
    - 🛣️ `Travel` = Distance × 2 × Emission Factor  
    - 🏠 `Home` = Based on Energy Type  
    - 🥗 `Diet` = Diet Type Emission Average  
    """)

# Recommendations
st.header("🌱 Greener Alternatives")
if travel_mode != "Walk":
    st.info("🚶 Consider walking or biking to drastically cut your travel emissions.")
if home_energy not in ["Solar", "Wind"]:
    st.info("🔋 Switching to renewable energy can slash your home's carbon impact.")
if diet_type != "Vegan":
    st.info("🥦 A plant-based diet reduces food emissions and improves health!")

# Carbon Offset
offset_cost = total_emission * 0.02
st.markdown(f"💸 Offset your emissions by donating ~**${offset_cost:.2f}** to certified carbon projects.")

# AI Summary
with st.expander("📘 Gemini AI Summary"):
    prompt = f"""
    The user travels {distance_km} km daily by {travel_mode}, uses {home_energy} energy, and eats a {diet_type} diet.
    Write a short, engaging summary of their environmental and health impact and what they could improve.
    """
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        st.markdown(response.text)
    except Exception as e:
        st.error(f"Gemini API Error: {e}")

# Footer
st.caption("🛠️ Built with 💚 using Streamlit, Gemini AI, and Matplotlib.")
