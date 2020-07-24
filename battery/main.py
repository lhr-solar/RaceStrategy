# main script for running race strat software

lap_length   = 5.513 # in kilometers
laps         = 60
distance     = lap_length * laps
max_speed    = 90    # kph
acceleration = 0
time         = 0     # hours

current_soc     = 100 # %, soc = state of charge
desired_end_soc =  10 # %, what we want the soc to be at the end

capacity             = 5   # KWh
desired_end_capacity = 0.5 # KWh

recharge_rate = 0.8 # KW

# battery_resistance = 0.1 # Ohms, add once current is found

# Assuming battery outputs 5KWh desired_end_soc implies = 0.5 KWH leftover

mass               =  227      # kg
gradient_angle     =    0      #
rolling_resistance =    0.020  # average for car tires on asphalt
drag_coefficient   =    0.256  # from thiago
air_density        =    1.225  # kg/m^3
cross_area         =    1.2    # m^2, from thiago
gravity            =    9.81   #


def main():


    # energy = 4.5 = 1/3600*[230*9.8*0.02 + 0.0386*1.225*0.25*2*v^2 ]*50

    high_velocity = 0

    for velocity in range(max_speed, 0, -1): # velocity in km/h
        time = distance / velocity
        gained_energy = recharge_rate * time # KWh 
        energy = (1/3600) * distance * ((mass * gravity * rolling_resistance) +
                 (0.0386 * air_density * drag_coefficient * cross_area * velocity ** 2) + # 0.0386 for km/h
                 (mass * acceleration))

        print(f"energy: {energy:2.3f} KW, velocity: {velocity:2.3f} km/h, energy gained: {gained_energy:2.3f} KW")
        if (not high_velocity and (capacity - energy + gained_energy) >= desired_end_capacity):
            high_velocity = velocity
            
        if(energy <= gained_energy): # find best coasting speed
            print("\nCoasting Speed: " + str(velocity))
            break

    print(f"Fastest Speed:  {high_velocity} km/h, Laps: {laps}")
    print(f"Total Distance: {distance} km")

    print(f"Recharge time: {calc_recharge_time(recharge_rate, 20, 2.5):0.3f} hours")


# return time to recharge battery while coasting
def calc_recharge_time(recharge_rate, coasting_velocity, current_capacity):
    upper_battery_capacity = 4.0 # KWh, point when to swap back to battery power
    
    time  = ((upper_battery_capacity - current_capacity) / 
            (recharge_rate - ((1/3600) * coasting_velocity * ((mass * gravity * rolling_resistance) +
            (0.0386 * air_density * drag_coefficient * cross_area * coasting_velocity ** 2) +
            (mass * acceleration)))))
    return time
        
main()
