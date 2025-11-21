#get key

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

#load LLM

from google import genai

client = genai.Client(api_key=api_key)

from google.genai import types

#import sys

import sys


#Main

def main():
    print("Hello from ai-agent!")
    if len(sys.argv) < 2:
        sys.exit("Error: No input detected!")
    user_prompt = sys.argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages,)
    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
