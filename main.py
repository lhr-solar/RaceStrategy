# main script for running race strat software

def main():
    lap_length   = 5.513  # in kilometers
    laps         = 14
    distance     = lap_length * laps
    max_speed    = 20    # kph
    acceleration = 0

    current_soc     = 100 # %, soc = state of charge
    desired_end_soc =  10 # %, what we want the soc to be at the end

    capacity             = 5   # KWh
    desired_end_capacity = 0.5 # KWh

    # Assuming battery outputs 5KWh desired_end_soc implies = 0.5 KWH leftover

    mass               = 1000      # kg
    gradient_angle     =    0      #
    rolling_resistance =    0.020  # average for car tires on asphalt
    drag_coefficient   =    0.250  # average for cars
    air_density        =    1.225  # kg/m^3
    cross_area         =    2      # m^2
    gravity            =    9.81   #

    # energy = 4.5 = 1/3600*[230*9.8*0.02 + 0.0386*1.225*0.25*2*v^2 ]*50

    for velocity in range(max_speed, 0, -1):
        energy = (1/3600) * distance * ((mass * gravity * rolling_resistance) +
                 (0.0386 * air_density * drag_coefficient * cross_area * velocity ** 2) + 
                 (mass * acceleration))

        print(f"energy: {energy}, velocity: {velocity}")
        if capacity - energy >= desired_end_capacity:
            print(f"\nfastest speed: {velocity}, laps: {laps}")
            break


main()
