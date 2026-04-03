# nasa_artemis_api.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY") 

def get_artemis_updates():
    """
    Retrieves the latest Artemis mission statuses. 
    Updated April 2026 following the successful launch of Artemis II.
    """
    # Updated Mission Log as of April 2, 2026
    missions = [
        {
            "name": "Artemis I",
            "status": "COMPLETED (December 2022)",
            "goal": "An uncrewed flight test of SLS and Orion, Artemis I Spent 25 days in space, completing a Distant Retrograde Orbit around the moon before splashing down into the Pacific Ocean.",
            "type": "Past"
        },
        {
            "name": "Artemis II",
            "status": "IN PROGRESS (Launched April 1, 2026)",
            "goal": "Artemis II is the first crewed mission of the Artemis program! Four astronauts are currently performing a 10-day lunar flyby to test life support systems onboard the Integrity Orion Capsule.",
            "type": "Past"
        },
        {
            "name": "Artemis III",
            "status": "Scheduled for 2027",
            "goal": "Now a Low Earth Orbit (LEO) rehearsal, Artemis III Will test docking and rendezvous between Orion and the SpaceX Starship HLS. The HLS (Human Landing System) will be used to land on the moon",
            "type": "Upcoming"
        },
        {
            "name": "Artemis IV",
            "status": "Targeting early 2028",
            "goal": "It will be official human return to the lunar surface! It will be the first mission to land humans on the Moon since Apollo 17 in 1972.",
            "type": "Upcoming"
        },
        {
            "name": "Artemis V",
            "status": "Targeting late 2028",
            "goal": "As the second human landing on the Moon, Artemis V will mark the beginning of deploying infrastructure on moon for a permanent human base on the lunar south pole",
            "type": "Upcoming"
        }
    ]

    try:
        # Retrieves images from the NASA Image API to stay dynamic
        response = requests.get("https://images-api.nasa.gov/search?q=Artemis&media_type=image")
        response.raise_for_status()
        items = response.json()["collection"]["items"]

        for i, mission in enumerate(missions):
            # Uses a placeholder for Artemis V (index 4) or if API fails
            if i == 4 or i >= len(items):
                mission["image"] = "assets/artemis_placeholder.jpeg"
            else:
                mission["image"] = items[i]["links"][0]["href"]

        return missions

    except Exception:
        # Fallback if API is down
        for mission in missions:
            mission["image"] = "assets/artemis_placeholder.jpeg"
        return missions