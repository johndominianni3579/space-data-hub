# nasa_artemis_api.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY") 

def get_artemis_updates():
    missions = [
        {"name": "Artemis I", "status": "COMPLETED (Dec 2022)", "goal": "Uncrewed test of SLS/Orion. Traveled 1.3 million miles."},
        {"name": "Artemis II", "status": "IN PROGRESS (Launched April 1, 2026)", "goal": "First crewed mission! Four astronauts are testing life support on a 10-day lunar flyby."},
        {"name": "Artemis III", "status": "Scheduled for 2027", "goal": "LEO rehearsal testing docking between Orion and SpaceX Starship HLS."},
        {"name": "Artemis IV", "status": "Targeting early 2028", "goal": "Official human return to the lunar surface! First landing since 1972."},
        {"name": "Artemis V", "status": "Targeting late 2028", "goal": "Sustainability phase. Deployment of the Lunar Gateway."}
    ]

    try:
        response = requests.get("https://images-api.nasa.gov/search?q=Artemis&media_type=image")
        response.raise_for_status()
        items = response.json()["collection"]["items"]

        # --- NEW ROBUST MAPPING LOGIC ---
        
        # 1. Extract URLs by searching Titles for keywords
        crew_url = "PLACEHOLDER"
        logo_url = "PLACEHOLDER"
        backup_url = "PLACEHOLDER"

        for item in items:
            title = item['data'][0].get('title', '').lower()
            href = item['links'][0]['href']
            
            # Find the Astronaut/Crew image
            if "crew" in title or "astronaut" in title:
                crew_url = href
            # Find the Logo/Artemis graphic
            elif "logo" in title or "graphic" in title:
                logo_url = href
            # Grab a generic one for Artemis III
            elif "orion" in title and backup_url == "PLACEHOLDER":
                backup_url = href

        # 2. Assign specifically to the mission names
        for m in missions:
            if m["name"] == "Artemis II":
                m["image"] = crew_url
            elif m["name"] == "Artemis III":
                m["image"] = backup_url if backup_url != "PLACEHOLDER" else items[0]['links'][0]['href']
            elif m["name"] == "Artemis IV":
                m["image"] = logo_url
            elif m["name"] == "Artemis V":
                m["image"] = "PLACEHOLDER"
            else:
                # Artemis I gets the very first result
                m["image"] = items[0]['links'][0]['href']

        return missions

    except Exception:
        for m in missions: m["image"] = "PLACEHOLDER"
        return missions