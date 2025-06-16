import os
import requests

def infer_plot_types_from_prompt(prompt: str) -> str:
    """
    Uses Gemini API to infer plot types from a user prompt.
    Returns a string describing the inferred plot types.
    """
    api_key = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + api_key
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": f"Given the following user prompt, infer what kinds of data plots (e.g., bar, line, scatter, pie, histogram, etc.) are needed. Just list the plot types. Prompt: {prompt}"}]}]
    }
    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        # Extract the text response from Gemini
        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return "Could not parse Gemini response."
    else:
        return f"Gemini API error: {response.status_code}"
