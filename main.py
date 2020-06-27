# main script for running race strat software

def main():
    distance = 50        # in kilometers
    max_speed = 40       # kph
    acceleration = 0
    d_factor = 3/25      # from 0.01 = d(5)(1/60)

    current_soc = 1000  # kWh, soc = state of charge
    desired_end_soc = 10  # kWh, what we want the soc to be at the end

    # energy = distance(d_factor * velocity^2 + acceleration)

    for velocity in range(max_speed, 0, -1):
        decrease = distance * (d_factor * velocity**2 + acceleration)
        print(f"decrease: {decrease}, velocity: {velocity}")
        if current_soc - decrease >= desired_end_soc:
            print(f"\nfastest speed: {velocity}")
            break


main()
