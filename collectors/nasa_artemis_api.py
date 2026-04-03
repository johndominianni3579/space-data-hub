# nasa_artemis_api.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY") 

def get_artemis_updates():
    # 1. Manual Log: Keeping your detailed 2026 descriptions
    missions = [
        {"name": "Artemis I", "status": "COMPLETED (Dec 2022)", "goal": "Uncrewed flight test..."},
        {"name": "Artemis II", "status": "IN PROGRESS (Launched April 1, 2026)", "goal": "First crewed mission..."},
        {"name": "Artemis III", "status": "Scheduled for 2027", "goal": "LEO Rehearsal..."},
        {"name": "Artemis IV", "status": "Targeting early 2028", "goal": "Human Lunar Landing..."},
        {"name": "Artemis V", "status": "Targeting late 2028", "goal": "Sustainability phase..."}
    ]

    try:
        response = requests.get("https://images-api.nasa.gov/search?q=Artemis&media_type=image")
        response.raise_for_status()
        items = response.json()["collection"]["items"]

        # --- THE SPECIFIC MAPPING OVERRIDES ---
        
        # 1. Store the Astronaut Image (Index 3 in your current API results)
        astronaut_img = items[3]["links"][0]["href"] if len(items) > 3 else "PLACEHOLDER"
        
        # 2. Store the Artemis Logo (Index 1 in your current API results)
        logo_img = items[1]["links"][0]["href"] if len(items) > 1 else "PLACEHOLDER"

        for i, m in enumerate(missions):
            if m["name"] == "Artemis II":
                # SETTING THE ASTRONAUT IMAGE HERE
                m["image"] = astronaut_img
            
            elif m["name"] == "Artemis III":
                # FILLING THE BLANK: Pulling from API Index 2
                m["image"] = items[2]["links"][0]["href"] if len(items) > 2 else "PLACEHOLDER"
                
            elif m["name"] == "Artemis IV":
                # SETTING THE LOGO IMAGE HERE
                m["image"] = logo_img
                
            elif m["name"] == "Artemis V":
                # KEEPING THE PLACEHOLDER
                m["image"] = "PLACEHOLDER"
                
            else:
                # DEFAULT: Artemis I stays at Index 0
                m["image"] = items[i]["links"][0]["href"] if i < len(items) else "PLACEHOLDER"

        return missions

    except Exception:
        for m in missions: m["image"] = "PLACEHOLDER"
        return missions