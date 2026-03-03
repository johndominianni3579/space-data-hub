import os

# apod.py

"""Fetches NASA's Astronomy Picture of the Day."""
# hello
import requests

def get_apod():
    api_key = os.getenv("NASA_API_KEY", "DEMO_KEY")
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    try:
        data = requests.get(url).json()
        return {
            "title": data.get("title"),
            "url": data.get("url"),
            "explanation": data.get("explanation"),
            "media_type": data.get("media_type")
        }
    except:
        return {"error": "APOD unavailable"} 