"""
main.py
====================================
The core module of the Lap Simulator
"""

import math
# main script for running race strat software

from solarpanel.main import main as solar_power
from car import Car
from IO import GetInputs
inputs = GetInputs()

lap_length = inputs['lap_length'] # in kilometers
laps       = int(inputs['laps'])
distance   = lap_length * laps
gravity    = 9.81  #m/s^2
    
def main():
    # energy = 4.5 = 1/3600*[230*9.8*0.02 + 0.0386*1.225*0.25*2*v^2 ]*50

    solar = Car(inputs)
    curr_time = 0
    dist_left = distance
    for lap in range(laps):
        print(f"In lap {lap}")
        # below desired end capacity, probably want to recharge
        if solar.current_capacity < solar.end_capacity:
            velocity = solar.coast_speed(lap_length)
            print(f"Travelling at coasting speed of {velocity}")

        else:
            velocity = solar.max_speed
            # velocity = solar.best_speed(lap_length)
            print(f"Travelling at driving speed of {velocity}")
        
        solar.update_capacity(velocity, lap_length)
        dist_left -= lap_length
        lap_time = lap_length / velocity
        curr_time += lap_time
        print(f"Current capacity: {(solar.current_capacity * 100) / solar.capacity}")
        print(f"Distance remaining: {dist_left}")
        print(f"Lap time: {lap_time}\n")
        
    print(f"\n\nEnd capacity: {solar.current_capacity}")
    print(f"Total time: {curr_time}")
    # print(f"Fastest Speed:  {high_velocity} km/h, Laps: {laps}")
    # print(f"Coasting Speed: {coast_velocity} km/h")
    # print(f"Total Distance: {distance} km")
    # print(f"Recharge time: {solar.calc_recharge_time():0.3f} hours")

main()