import os
import requests

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

def get_ai_response(prompt):
    url = "https://api.together.xyz/inference"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "prompt": prompt,
        "max_tokens": 100
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json().get("output", "Sorry, I couldn’t understand.")
    except:
        return "⚠️ AI service failed."