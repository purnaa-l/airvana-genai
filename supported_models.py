import google.generativeai as genai
import os

# Set your Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# List available models
models = genai.list_models()

for model in models:
    print(f"Name: {model.name}")
    print(f"  Description: {model.description}")
    print(f"  Supported generation methods: {model.supported_generation_methods}")
    print("-" * 50)
