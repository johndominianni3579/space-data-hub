# apod.py

"""Fetches NASA's Astronomy Picture of the Day."""

import requests

def get_apod():
    url = "https://api.nasa.gov/planetary/apod?api_key=MQqhXmbciRwp3UH6s1aYTPQisHSAZOS0ef1zOW7n"
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