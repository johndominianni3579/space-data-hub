# rocket_specs.py
 
"""
    Retrieves the specifications of the SpaceX fleet including the active status, number of stages, height, mass, thrust, and roadmaps for Starship.
    
    Returns a list of dictionaries containing the rocket specifications.
    If an error occurs, returns a dictionary containing a single key-value pair with the key 'error' and a value describing the error.
"""

import requests

def get_spacex_fleet():
    url = "https://api.spacexdata.com/v4/rockets"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        fleet_data = []
        for rocket in data:
            name = rocket.get("name")

            rocket_info = {
                "name": name,
                "active": "Yes" if rocket.get("active") else "No",
                "stages": rocket.get("stages", "N/A"),
                "height_m": f"{rocket['height']['meters']}m",
                "mass_kg": f"{rocket['mass']['kg']:,} kg",
                "thrust_vac_kn": f"{rocket['engines']['thrust_vacuum']['kN']:,} kN",
                "description": rocket.get("description"),
                "wiki_url": rocket.get("wikipedia"),
                "image": rocket["flickr_images"][0] if rocket.get("flickr_images") else "No Image Available"
            }

            # Provides roadmap for starship (roadmap to Moon + Mars)
            if name == "Starship":
                rocket_info["roadmap"] = {
                    "March 2026": "Flight 12 (First V3 Launch & Tower Catch Attempt)",
                    "June 2026": "Orbital Propellant Transfer Demo",
                    "Late 2026": "Uncrewed Mars Landing Window",
                    "2027": "Artemis III Earth-Orbit Docking Test"
                }
            
            fleet_data.append(rocket_info)
            
        return fleet_data
    except Exception as e:
        return {"error": f"Rocket Specs API connection failed: {e}"}