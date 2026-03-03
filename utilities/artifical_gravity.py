import math

def calculate_gravity(radius_meters):
    """
    Calculates RPM needed for 1G (Earth Gravity) at a given radius.
    Formula: RPM = (30/pi) * sqrt(9.81 / radius)
    """
    if radius_meters <= 0:
        return "Error: Radius must be greater than zero."
    
    # Standard Earth Gravity is 9.80665 m/s^2
    g = 9.80665
    
    # Calculate RPM
    rpm = (30 / math.pi) * math.sqrt(g / radius_meters)
    return round(rpm, 2)