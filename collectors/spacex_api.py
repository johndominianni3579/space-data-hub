# SpaceX API to gather information on SpaceX ongoing missions
# These missions include scheduled launches, satellite deployment missions, and space exploration missions

import requests

def get_next_launch():
    """
    Retrieves the soonest upcoming launch for SpaceX Rockets.
    
    Returns a dictionary containing the name, date, and details of the soonest SpaceX launch.
    If an error occurs, returns a dictionary containing a single key-value pair with the key 'error' and a value describing the error.
    """
    try:
        # Best API for upcoming SpaceX updates. SpaceX itself does not provide API's.
        url = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/?search=SpaceX"
        response = requests.get(url).json()
        
        # soonest upcoming launch for SpaceX Rockets
        first_launch = response['results'][0]
        
        # returns name, date, and details of earliest upcoming SpaceX launch
        return {
            "name": first_launch['name'],
            "date": first_launch['net'], # 'NET' stands for 'No Earlier Than'
            "details": first_launch['mission']['description'] if first_launch['mission'] else "Mission details pending."
        }
    except Exception as e:
        return {"error": "API Limit reached or sync error. Check internet connection."}