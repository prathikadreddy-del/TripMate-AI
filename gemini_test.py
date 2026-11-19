

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

print("Connecting to Gemini...\n")

for chunk in client.models.generate_content_stream(
    model="gemini-3.8-flash",
    contents="Introduce yourself as my AI agent in just 2 sentences."
):
    if chunk.text:
        print(chunk.text, end="", flush=True)

print("\n\nResponse completed!")


