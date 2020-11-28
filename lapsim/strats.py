# from config import ureg

# carl - stays bounded within a certain battery capacity, better for longer distances
def carl (solar, max_speed, angle, time, dist_left, count, old_velocity):
    # below desired end capacity, probably want to recharge
    if solar.current_capacity < solar.end_capacity:
        velocity = solar.coast_speed(angle)
        if (angle >= 0.5): # going uphill
            velocity -= 2.5
        result = f"Travelling at coasting speed of {velocity} km/h\n"
    else:
        velocity = max_speed
        if (angle >= 0.5): # going uphill
            velocity -= 2.5
        elif (angle <= -0.5 and max_speed < 80): # going downhill
            velocity += 7
        result = f"Travelling at driving speed of {velocity} km/h\n"

    return result, velocity, old_velocity

# carlos - drive fast no coast, better for shorter distances
def carlos (solar, max_speed, angle, time, dist_left, section, old_velocity):
    result = f"Travelling at driving speed of {max_speed} km/h"

    print(f"charge_lvl: {solar.start_capacity} and solar.start_capacity: {solar.current_capacity}")
    if section == 0 and solar.current_capacity <= \
        (solar.start_capacity + solar.end_capacity) / 2: # push to 10%
        print("made it here")
        
        result += " - pitted and recharged"

        charge_lvl = solar.start_capacity

        if (charge_lvl > solar.current_capacity):
            print("call this")
        result += "\n"
        return result, 0, 0
        
    result += "\n"
    print("this is still called")
    
    return result, max_speed, old_velocity

# carson - pits if it needs to
def carson (solar, max_speed, angle, time, dist_left, section, old_velocity):
    result = f"Travelling at driving speed of {max_speed} km/h"

    if section == 0 and solar.current_capacity <= \
        (solar.start_capacity + solar.end_capacity) / 2: # push to 10%
        
        result += " - pitted and recharged"

        charge_lvl = solar.start_capacity

        if (charge_lvl > solar.current_capacity):
            result += "\n"
            return result, 0, 0

    else:
        # below desired end capacity, probably want to recharge
        if solar.current_capacity < solar.end_capacity:
            velocity = solar.coast_speed(angle)
            if (angle >= 0.5): # going uphill
                velocity -= 2.5
            result = f"Travelling at coasting speed of {velocity} km/h\n"
        else:
            velocity = max_speed
            if (angle >= 0.5): # going uphill
                velocity -= 2.5
            elif (angle <= -0.5 and max_speed < 80): # going downhill
                velocity += 7
            result = f"Travelling at driving speed of {velocity} km/h\n"

        return result, velocity, old_velocity
        
    result += "\n"
    
    return result, max_speed, old_velocity