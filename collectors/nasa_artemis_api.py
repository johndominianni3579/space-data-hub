# nasa_artemis_api.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY") 

def get_artemis_updates():
    missions = [
        {"name": "Artemis I", "status": "COMPLETED (Dec 2022)", "goal": "Uncrewed flight test of SLS and Orion. Spent 25 days in space and traveled 1.3 million miles."},
        {"name": "Artemis II", "status": "IN PROGRESS (Launched April 1, 2026)", "goal": "First crewed mission! Four astronauts are performing a 10-day lunar flyby."},
        {"name": "Artemis III", "status": "Scheduled for 2027", "goal": "LEO rehearsal testing docking between Orion and SpaceX Starship HLS."},
        {"name": "Artemis IV", "status": "Targeting 2028", "goal": "Official human return to the lunar surface! First landing since 1972."},
        {"name": "Artemis V", "status": "Future Mission", "goal": "Sustainability phase. Deployment of the Lunar Gateway."}
    ]

    try:
        response = requests.get("https://images-api.nasa.gov/search?q=Artemis&media_type=image")
        response.raise_for_status()
        items = response.json()["collection"]["items"]

        # 1. HELPER: Find the best image by searching for a keyword in the NASA title/description
        def find_img(keyword):
            for item in items:
                description = str(item.get("data", [{}])[0].get("description", "")).lower()
                title = str(item.get("data", [{}])[0].get("title", "")).lower()
                if keyword in description or keyword in title:
                    return item["links"][0]["href"]
            return "PLACEHOLDER"

        # 2. MANUALLY ASSIGN THE IMAGES
        # Find the astronaut/crew image for Artemis II
        crew_img = find_img("crew") 
        if crew_img == "PLACEHOLDER": crew_img = find_img("astronaut") # Fallback search

        # Find the logo/graphic for Artemis IV
        logo_img = find_img("logo")
        if logo_img == "PLACEHOLDER": logo_img = items[1]["links"][0]["href"] # Fallback to index 1

        for i, m in enumerate(missions):
            if m["name"] == "Artemis II":
                m["image"] = crew_img
            elif m["name"] == "Artemis IV":
                m["image"] = logo_img
            elif m["name"] == "Artemis III":
                # Fills the blank: Pulls whatever is at index 2 (usually a rocket or assembly shot)
                m["image"] = items[2]["links"][0]["href"] if len(items) > 2 else "PLACEHOLDER"
            elif m["name"] == "Artemis V":
                m["image"] = "PLACEHOLDER"
            else:
                # Default for Artemis I
                m["image"] = items[i]["links"][0]["href"] if i < len(items) else "PLACEHOLDER"

        return missions

    except Exception:
        for m in missions: m["image"] = "PLACEHOLDER"
        return missions