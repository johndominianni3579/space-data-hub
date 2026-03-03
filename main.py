# main.py 

"""
This file serves as the main entry point for my 2026 Space Hub application.
It prints out a welcome message and displays information about ongoing space projects from various APIs.
It gathers all of the information for the dashboard from the collectors and utilities modules.
"""

# import all necessary files (collectors and utilities)
from collectors.spacex_api import get_next_launch
from collectors.nasa_artemis_api import get_artemis_updates
from collectors.rocket_specs import get_spacex_fleet
from collectors.nasa_visuals import get_apod
from collectors.asteroids import get_nearby_asteroids
from utilities.artifical_gravity import calculate_gravity
from utilities.mars_trip_duration import calculate_mars_trip

def run_dashboard():
    """
    Prints out the welcome message and displays the information about ongoing space projects from various APIs.
    
    The information includes:
    - NASA's Astronomy Picture of the Day
    - The next SpaceX mission and its launch date
    - The upcoming Artemis missions and their status/goals
    - The specifications of the SpaceX fleet including the active status, number of stages, height, mass, thrust, and roadmaps for Starship
    """
    print("Welcome to the 2026 Space Hub -- to learn about all ongoing space projects!!!")

    # 1. NASA Picture of the Day
    apod = get_apod()
    print("\n" + "="*40)
    print("NASA APOD")
    print("="*40)
    print(f"Title: {apod.get('title')}")
    print(f"URL: {apod.get('url')}")
    print(f"Explanation: {apod.get('explanation')}")
    print(f"Media Type: {apod.get('media_type')}")

    # 2. Asteroid Info of the Day
    print("\n" + "="*40)
    print("Asteroid Info of the Day")
    print("="*40)
    asteroids = get_nearby_asteroids()
    if not asteroids:
        print("No asteroid data returned. Check API date formatting.")
    for asteroid in asteroids:
        print(f"Asteroid: {asteroid.get('name')}")
        print(f"Hazardous: {asteroid.get('hazard')}")
        print(f"Velocity: {asteroid.get('velocity_kph')} kph")
        print(f"Miss Distance: {asteroid.get('miss_dist_km')} km")
        print()

    # 3. SpaceX Launch Data
    launch = get_next_launch()
    print(f"\n[Next SpaceX Mission]: {launch.get('name')}")
    print(f"Launch Date: {launch.get('date')}")

    # 4. Artemis Mission Data
    artemis_missions = get_artemis_updates()
    for mission in artemis_missions:
        print(f"\n[Upcoming Artemis Mission]: {mission.get('name')}")
        print(f"Status: {mission.get('status')}")
        print(f"Goal: {mission.get('goal')}")

    # 5. SpaceX Rocket Specifications
    print("\n" + "="*40)
    print("SPACEX FLEET SPECIFICATIONS")
    print("="*40)
    
    fleet = get_spacex_fleet()
    if isinstance(fleet, list):
        for rocket in fleet:
            print(f"Rocket: {rocket['name']}")
            print(f"Active: {rocket['active']}")
            print(f"Stages: {rocket['stages']}")
            print(f"Height: {rocket['height_m']}")
            print(f"Mass: {rocket['mass_kg']}")
            print(f"Thrust: {rocket['thrust_vac_kn']}")
            
            if "roadmap" in rocket:
                print("2026-2027 Roadmap:")
                for date, event in rocket["roadmap"].items():
                    print(f"  • {date}: {event}")
            print("-" * 20)
    else:
        print(f"Error: {fleet.get('error')}")

    # 6. Artificial Gravity Calculator
    print("ARTIFICIAL GRAVITY CALCULATOR -- to determine RPM needed for 1G (Earth Gravity) at a given radius for a spacecraft.")
    print("\n" + "="*40)
    
    try:
        user_radius = float(input("Enter the radius of your spacecraft in meters: "))

        result = calculate_gravity(user_radius)
        
        if isinstance(result, str):
            print(result)
        else:
            print(f"\n[Result]: To achieve 1G at a {user_radius}m radius,")
            print(f"your spacecraft must rotate at {result} RPM.")
            
    except ValueError:
        print("Invalid input! Please enter a numerical value for the radius.")

    # 7. Mars Voyage Duration Calculator 
    print("\n" + "="*40)
    print("MARS VOYAGE DURATION CALCULATOR -- to determine travel time to Mars.")
    print("="*40)
    print("The default transit speed is ~28,000 kph (Chemical Rockets).")
    print("Future rocket-spacecraft systems will be able to travel faster")
    print("Enter your own speed to see how long a hypothetical trip would take!")
    
    try:
        user_speed = input("Enter your spacecraft speed in kph (or press Enter for default): ")

        if user_speed == "":
            speed = 28000
        else:
            speed = float(user_speed) 
            
        trip = calculate_mars_trip(speed)
        
        if isinstance(trip, str):
            print(trip)
        else:
            print(f"\nVoyage Statistics at {trip['speed']}:")
            print(f"Total Travel Time: {trip['days']} Days")
            print(f"Approximate Duration: {trip['months']} Months")
            
    except ValueError:
        print("Invalid input! Please enter a number for the speed.")

if __name__ == "__main__":
    run_dashboard()