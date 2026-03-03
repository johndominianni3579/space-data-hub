import requests
from datetime import datetime

def get_nearby_asteroids():
    """
    Retrieves a list of nearby asteroids from NASA's NeoWs API.
    Includes a fallback mechanism to ensure data is returned even if 
    today's specific records haven't been posted yet.
    """
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={today}&api_key=MQqhXmbciRwp3UH6s1aYTPQisHSAZOS0ef1zOW7n"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 429:
            return [{"name": "API Limit Reached", "hazard": "N/A", "velocity_kph": "0", "miss_dist_km": "0"}]
            
        data = response.json()
        neos_all = data.get("near_earth_objects", {})
        
        neos_today = []
        if today in neos_all:
            neos_today = neos_all[today]
        elif neos_all:
            available_dates = sorted(neos_all.keys(), reverse=True)
            neos_today = neos_all[available_dates[0]]
        
        if not neos_today:
            return []

        summary = []
        for obj in neos_today[:5]:
            close_data = obj.get('close_approach_data', [{}])[0]
            
            summary.append({
                "name": obj.get("name", "Unknown Asteroid"),
                "hazard": "YES" if obj.get("is_potentially_hazardous_asteroid") else "No",
                "velocity_kph": f"{float(close_data.get('relative_velocity', {}).get('kilometers_per_hour', 0)):,.2f}",
                "miss_dist_km": f"{float(close_data.get('miss_distance', {}).get('kilometers', 0)):,.0f}"
            })
        return summary

    except Exception as e:
        print(f"Asteroid API Error: {e}")
        return []