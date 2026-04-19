import os
from dotenv import load_dotenv
from google import genai

def list_models():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("API Key not found")
        return
    
    client = genai.Client(api_key=api_key)
    try:
        print("Available models:")
        for m in client.models.list():
            if 'generateContent' in m.supported_actions:
                print(m.name)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    list_models()
