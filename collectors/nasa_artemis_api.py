import requests
import os
from dotenv import load_dotenv

# loads key from .env
load_dotenv()
API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY") 

import requests

def get_artemis_updates():
    """
    Combines live NASA Image Library data with a manual 2026 Mission Log.
    Unofrtunately, Artemis launch info is currently very chaotic in the API's because of the postponement of Artemis II.
    """
    # 1. Manual Log (The facts as of March 1, 2026)
    manual_log = {
        "Artemis II": "VAB Repairs (Helium leak fix). Launch window moved to April 2026.",
        "Artemis III": "Now an LEO Rehearsal (Docking test) of the Orion Spacecraft with the SpaceX Starship. Launch scheduled for 2027. No lunar landing.",
        "Artemis IV": "Targeting 2028. Now the official mission for the first human lunar landing using the Spacex HLS (Human Landing System)."
    }

    try:
        # 2. Get images from the API
        response = requests.get("https://images-api.nasa.gov/search?q=Artemis&media_type=image")
        response.raise_for_status()
        data = response.json()
        items = data["collection"]["items"]

        final_missions = []
        
        # 3. Merge the manual log with the API results
        for i, (name, status) in enumerate(manual_log.items()):
            # Try to find a specific image from the API results, or use a default
            img_url = items[i]["links"][0]["href"] if i < len(items) else "No image found"
            
            final_missions.append({
                "name": name,
                "status": status,
                "goal": "Human Lunar Exploration Program",
                "image": img_url
            })

        return final_missions

    except Exception as e:
        # Returns data regardless of API failure
        return [{"name": k, "status": v, "goal": "Manual Fallback"} for k, v in manual_log.items()]