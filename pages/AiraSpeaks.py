# import streamlit as st
# import google.generativeai as genai
# from gtts import gTTS
# from pydub import AudioSegment
# from tempfile import NamedTemporaryFile
# import os
# import re
# from dotenv import load_dotenv

# load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# model = genai.GenerativeModel('gemini-2.5-flash')

# st.set_page_config(page_title="Aira – Your Podcast Companion", layout="centered", page_icon="🎧")
# st.markdown("""
# <style>
# [data-testid="stAppViewContainer"] {
#     background-image: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e');
#     background-size: cover;
#     background-attachment: fixed;
#     background-position: center;
# }
# [data-testid="stHeader"], [data-testid="stSidebar"] {
#     background: rgba(0,0,0,0);
# }
# .stButton > button {
#     background-color: #4CAF50;
#     color: white;
#     padding: 14px 30px;
#     border: none;
#     border-radius: 12px;
#     font-size: 20px;
#     font-weight: bold;
#     box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
#     transition: 0.3s ease;
# }
# .stButton > button:hover {
#     background-color: #388E3C;
#     transform: scale(1.05);
# }
# h1 {
#     text-align: center;
#     color: #ffffff;
#     font-size: 48px;
#     font-weight: 800;
#     margin-top: 20px;
# }
# h3 {
#     text-align: center;
#     color: #ffffff;
#     font-weight: 400;
# }
# </style>
# """, unsafe_allow_html=True)
# st.markdown("<h1>🎙 Welcome to AiraSpeaks!</h1>", unsafe_allow_html=True)
# st.markdown("<h3>Aira: AirVana’s intuitive podcast engine – immersive, eloquent, effortless.</h3>", unsafe_allow_html=True)
# styles = {
#     "Breezy Science Teacher": "speak like a breezy, friendly science teacher",
#     "Serious News Reporter": "formal tone like a news anchor",
#     "Explaining to a Student": "simple, educational tone for a beginner",
#     "Witty Comedian": "funny, light, and quirky tone",
# }
# query = st.text_input("🌍 What should Aira talk about?", "Air Pollution and their Rising Impact?")
# style = st.selectbox("🎤 Pick Aira's podcast vibe", list(styles.keys()))
# def clean_text(text):
#     text = re.sub(r'\([^)]*\)', '', text)
#     text = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', text)
#     text = re.sub(r'[^\x00-\x7F]+', '', text)
#     text = re.sub(r'\bhost\b', '', text, flags=re.IGNORECASE)
#     return text.strip()
# def mix_intro_with_voice(intro_music_path, voice_path, output_path):
#     intro = AudioSegment.from_file(intro_music_path)[:10000].fade_out(1500)
#     voice = AudioSegment.from_file(voice_path)
#     combined = intro + voice
#     combined.export(output_path, format="mp3")

# if st.button("🎙 Generate Podcast Now!"):
#     with st.spinner("Aira is crafting your perfect audio experience..."):
#         aira_intro = "Hi, I'm Aira, AirVana's intuitive podcast. Dive into a seamless audio experience crafted just for you. "
#         prompt = f"""
#         You are Aira, AirVana’s intelligent podcast voice. {styles[style]}.
#         Topic: {query}.
#         Be voice-friendly and engaging. Include verbal stage cues (pause), (soft music), etc.
#         Never say 'host'. Create content of only 150 words."
#         """
#         response = model.generate_content(prompt)
#         script = response.text.strip()
#         script = clean_text(script)
#         full_voice = aira_intro + " " + script + " " + "Thank you for listening to AiraSpeaks. We hope you enjoyed this episode. Stay tuned for more insights and stories. Signing off, Aira." 
#         tts = gTTS(text=full_voice, lang='en')
#         with NamedTemporaryFile(delete=False, suffix='.mp3') as voice_fp:
#             voice_path = voice_fp.name
#             tts.save(voice_path)

#         intro_music_path = "intro_music.mp3"  # 🎵 Ensure this exists
#         final_audio_path = "aira_final_podcast.mp3"
#         if os.path.exists(intro_music_path):
#             mix_intro_with_voice(intro_music_path, voice_path, final_audio_path)
#             st.success("🔊 Your podcast is ready!")
#             st.audio(final_audio_path)
#         else:
#             st.warning("⚠️ Intro music not found. Playing voice-only version.")
#             st.audio(voice_path)
