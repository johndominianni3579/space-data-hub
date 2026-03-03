# mars_trip_duration.py

"""
    Calculates travel time to Mars based on average distance.
    Default speed is roughly a modern chemical rocket's cruise speed.
"""

def calculate_mars_trip(speed_kph=28000):
    # Average distance to Mars is ~225 million km
    avg_distance = 225000000 
    
    hours = avg_distance / speed_kph
    days = hours / 24
    months = days / 30.44 # Average month length
    
    return {
        "days": round(days, 1),
        "months": round(months, 1),
        "speed": f"{speed_kph:,} kph"
    }