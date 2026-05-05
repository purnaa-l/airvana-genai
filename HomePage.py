import streamlit as st
st.set_page_config(
    page_title="AeroAI - AirVana's GenAI Powered Assistant!",
    page_icon="🌌",
    layout="centered"
)

page_bg_img = """
<style>
/* Background */
[data-testid="stAppViewContainer"] {
    background-size: cover;
    background-position: center;
    background-image: url('https://cdn.pixabay.com/photo/2021/11/01/19/39/nature-6761493_1280.jpg');
    # background-image: url('https://images.unsplash.com/photo-1743878206228-5f36b5f5c830?q=80&w=3087&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
    background-attachment: fixed;
}

/* Transparent header and sidebar */
[data-testid="stHeader"], [data-testid="stSidebar"] {
    background: rgba(0,0,0,0);
}

/* Fancy Titles */
h1 {
    color: #ffffff;
    font-size: 3em;
    font-weight: bold;
    text-shadow: 2px 2px 6px #b7d7a8;
}
h3 {
    color: #ffffff;
    font-size: 1.8em;
    text-shadow: 1px 1px 4px #a5d6a7;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #a8d5ba, #d7f2ba);
    color: #3e4e2c;
    border-radius: 12px;
    padding: 15px;
    font-size: 1.05em;
    font-weight: bold;
    border: none;
    width: 100%;
    margin-bottom: 18px;
    box-shadow: 0px 4px 10px rgba(62, 78, 44, 0.2);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #d7f2ba, #a8d5ba);
    transform: translateY(-4px);
    box-shadow: 0px 6px 15px rgba(62, 78, 44, 0.4);
}

/* Footer */
footer {
    font-size: 0.9em;
    color: #5c7c49;
    text-align: center;
    margin-top: 50px;
    font-weight: bold;
    text-shadow: 1px 1px 4px #c5e1a5;
}

/* Chat Bubble */
.chat-bubble {
    position: fixed;
    bottom: 30px;
    right: 30px;
    background: linear-gradient(135deg, #a8d5ba, #d7f2ba);
    color: #3e4e2c;
    border-radius: 50%;
    padding: 18px 22px;
    font-size: 28px;
    box-shadow: 0 6px 12px rgba(62, 78, 44, 0.4);
    cursor: pointer;
    z-index: 9999;
    transition: all 0.3s ease-in-out;
    text-align: center;
}
.chat-bubble:hover {
    background: linear-gradient(135deg, #d7f2ba, #a8d5ba);
    transform: scale(1.1);
}

/* Titles */
.fancy-title {
    text-align: center;
    color: #ffffff;
    font-size: 2.8em;
    font-weight: 700;
    margin-bottom: 0.5em;
    text-shadow: 2px 2px 6px #c5e1a5;
}
.subheading {
    text-align: center;
    color: #ffffff;
    font-size: 1.5em;
    margin-top: -1em;
    font-weight: 400;
    text-shadow: 1px 1px 4px #aed581;
}


</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


# --- Welcome Title ---
st.markdown("<h1 class='fancy-title'>Welcome to AeroAI 🌳🌱</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='subheading'>AirVana's Smart GenAI Assistant🌍</h3>", unsafe_allow_html=True)

# --- Divider ---
st.write("")
st.divider()

# --- Feature Cards ---
st.markdown("### 🌟 Where would you like to venture?", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("🌱 Smart Pollution Detector"):
        st.switch_page("pages/Polluscan.py")
    if st.button("💬 Health Impact Chatbot"):
        st.switch_page("pages/HealthifyAI.py")
    if st.button("📰 Live Environmental News"):
        st.switch_page("pages/EcoNews.py")
    # if st.button("🎙️ Interactive Voice AQI Assistant"):
    #     switch_page("voice_assistant")

with col2:
    if st.button("🌌 EarthLens - Natural Events Viewer"):
     st.switch_page("pages/EarthLens.py")
    #     switch_page("aira_speaks")
    if st.button("🎙️ Interactive Voice AQI Assistant"):
        st.switch_page("pages/VoiceAssistant.py")
    if st.button("🌳 EcoImpact - Real Time Simluator"):
        st.switch_page("pages/EcoImpact.py")
    # if st.button("🛡️ Personalized Health & Safety Tips"):
    #     switch_page("health_safety_tips")

# --- Footer ---
st.write("")
st.divider()

st.markdown("""
<footer class="footer">
    <p style="color: #ffffff;">&copy; 2025 AeroAI. All rights reserved.</p>
    <p style="color: #ffffff;">Developed by AirVana Team 🌱</p>
</footer>
""", unsafe_allow_html=True)


chat_bubble_html = """
<div class="chat-bubble" onclick="window.location.href='./voice_assistant';">
    💬
</div>
"""
st.markdown(chat_bubble_html, unsafe_allow_html=True)


#How to run?
#streamlit run HomePage.py 