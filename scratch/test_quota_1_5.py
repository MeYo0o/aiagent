import os
from dotenv import load_dotenv
from google import genai

def test_quota():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("API Key not found")
        return
    
    client = genai.Client(api_key=api_key)
    try:
        print("Testing gemini-1.5-flash...")
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents="Say hi"
        )
        print("Success (1.5-flash):", response.text)
    except Exception as e:
        print("Error (1.5-flash):", e)

if __name__ == "__main__":
    test_quota()
