import google.generativeai as genai
import pandas as pd
import speech_recognition as sr
import streamlit as st
import time
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")
chat = model.start_chat()

recognizer = sr.Recognizer()

st.set_page_config(page_title="🌌 Voice Chatbot", page_icon="💬", layout="wide")

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    background-image: url('https://images.unsplash.com/photo-1609042191775-746c6eeae7bc?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
}
[data-testid="stHeader"], [data-testid="stSidebar"] {
    background: rgba(0,0,0,0);
}
.chat-bubble {
    position: fixed;
    bottom: 30px;
    right: 30px;
    background-color: #6a0dad;
    color: white;
    border-radius: 50%;
    padding: 15px 20px;
    font-size: 24px;
    box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    cursor: pointer;
    z-index: 9999;
    transition: background 0.3s;
}
.chat-bubble:hover {
    background-color: #8a2be2;
}
.typing {
    font-style: italic;
    animation: blink 1s infinite;
}
@keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center; color: #F5F5F5;'>🌬️ Meet Airi – Your Voice & Text AI Companion 💬</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #D3D3D3;'> AirVana's GenAI assistant for smarter, healthier breathing 🌿. </p>", unsafe_allow_html=True)
st.divider()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

csv_file = "chat_history.csv"
if not os.path.exists(csv_file):
    pd.DataFrame(columns=["Role", "Content"]).to_csv(csv_file, index=False)

def store_chat(role, content):
    new_row = pd.DataFrame({"Role": [role], "Content": [content]})
    new_row.to_csv(csv_file, mode='a', header=False, index=False)
# Display Chat History
def display_chat():
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(f"🧑‍💬 {message['content']}")
        elif message["role"] == "model":
            with st.chat_message("assistant"):
                st.markdown(f"🤖 {message['content']}")

display_chat()

if len(st.session_state.chat_history) == 0:
     st.session_state.chat_history.append({"role": "model", "content": "Hi, I am Airi: AirVana's GenAI-powered intelligent assistant, how can I help you today?"})
     store_chat("Assistant", "Hi, I am Airi! I am AirVana's GenAI-powered intelligent assistant, how can I help you today?")

col1, col2, col3 = st.columns([1, 1, 1])  
with col2:
    input_type = st.radio("How do you want to converse with me?", ["Text", "Voice"], horizontal=True)
user_input_text = None
if input_type == "Text":
    user_input_text = st.text_input("", placeholder="Click here to type your message...", label_visibility="collapsed", key="text_input")
elif input_type == "Voice":
    if st.button("🎙️ Speak Now"):
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                st.info("Listening...")
                audio = recognizer.listen(source, timeout=5)
                user_input_text = recognizer.recognize_google(audio)
                st.success(f"You said: {user_input_text}")
            except sr.UnknownValueError:
                st.error("Couldn't understand. Try again!")
            except sr.RequestError:
                st.error("Service down. Try later.")
            except TimeoutError:
                st.error("Timeout. Speak quickly!")

def send_message(user_input):
    if user_input:
        with st.empty():
            st.markdown('<p class="typing">Airi is responding...</p>', unsafe_allow_html=True)
            time.sleep(1.5)  # Delay for realistic typing feel
        try:
            response = chat.send_message(user_input)
            return response.text
        except Exception as e:
            st.error(f"Error: {e}")
            return None
    return None

if user_input_text:
    if user_input_text.lower() in ["exit", "quit", "bye"]:
        st.success("👋 Goodbye! See you soon.")
        st.balloons()
    else:
        st.session_state.chat_history.append({"role": "user", "content": user_input_text})
        store_chat("User", user_input_text)

        response_text = send_message(user_input_text)
        if response_text:
            st.session_state.chat_history.append({"role": "model", "content": response_text})
            store_chat("Assistant", response_text)
            time.sleep(1)
            st.rerun()

chat_bubble_html = """
<div class="chat-bubble">
    💬
</div>
"""
st.markdown(chat_bubble_html, unsafe_allow_html=True)