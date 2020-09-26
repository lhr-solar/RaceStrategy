# from config import ureg

# carl - stays bounded within a certain battery capacity, better for longer distances
def carl (solar, max_speed, angle, length, count):
    # below desired end capacity, probably want to recharge
    if solar.current_capacity < solar.end_capacity:
        velocity = solar.coast_speed(length, angle)
        if (angle <= -0.5): # going downhill
            velocity += 5
        elif (angle >= 0.5): # going uphill
            velocity -= 2.5
        result = f"Travelling at coasting speed of {velocity} km/h\n"
    else:
        velocity = max_speed
        if (angle >= 0.5): # going uphill
            velocity -= 2.5
        elif (angle <= -0.5 and max_speed < 80): # going downhill
            velocity += 7
        result = f"Travelling at driving speed of {velocity} km/h\n"

    return result, velocity, 0

# carlos - drive fast no coast, better for shorter distances
def carlos (solar, max_speed, angle, dist_left, section):
    # pit time
    # max_speed = 90
    time = 0
    result = f"Travelling at driving speed of {max_speed} km/h"

    if section == 0 and solar.current_capacity <= 0.5: # push to 10%
        result += " - pitted and recharged"

        charge_lvl = (5.2/5) * dist_left * solar.capacity

        if (charge_lvl > solar.current_capacity):
            time = solar.calc_recharge_time(charge_lvl) # charge to 100
            solar.current_capacity = charge_lvl
        
    result += "\n"
    
    return result, max_speed, time

# carson - pits if it needs to
