import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
print(f"Using Key: {API_KEY[:5]}...")

genai.configure(api_key=API_KEY, transport='rest')

print("Listing models...")
try:
    with open("manual_result.txt", "w") as f:
        for m in genai.list_models():
            f.write(f"Model: {m.name}\n")
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
except Exception as e:
    with open("manual_result.txt", "w") as f:
        f.write(f"Error: {e}")
