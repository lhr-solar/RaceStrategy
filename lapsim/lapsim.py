"""
main.py
====================================
The core module of the Lap Simulator
"""

import math

from solarpanel.main import main as solar_power

from car import Car
import inputs

user_inputs = inputs.get_inputs()
# lap_length = user_inputs["lap_length"] # km
lap_length = 0
laps       = int(user_inputs['laps'])

track = []

with open("track.txt") as f:
    lines = f.readlines()
    for line in lines:
        var = line.strip().split(",")
        length = float(var[0])
        lap_length += length
        angle  = float(var[1])
        track.append([length, angle])
f.close()

distance   = lap_length * laps

def construct():
    """ The core code of the Lap Simulator

    Reads inputs from the inputs.txt file and runs the simulation based off of 
    those parameters. If some paramters are missing it fills them with defualt 
    values.

    Creates an output.txt file containing information about the simulation
    based on the passed inputs, including individual lap information as well as
    overall time, speed, and length of the race.
    """
    
    # gravity    = 9.81  #m/s^2
    # energy = 4.5 = 1/3600*[230*9.8*0.02 + 0.0386*1.225*0.25*2*v^2 ]*50

    solar = Car(user_inputs)
    solar.recharge_rate = solar_power()
    return solar

def run(solar, max_speed):
    curr_time = 0
    dist_left = distance
    for lap in range(laps):
        print(f"In lap {lap}")
        for straight in track:
            length = straight[0]
            angle  = straight[1]
            # below desired end capacity, probably want to recharge
            if solar.current_capacity < solar.end_capacity and angle >= 0:
                velocity = solar.coast_speed(length, angle)
                print(f"Travelling at coasting speed of {velocity}")

            else:
                velocity = max_speed
                # velocity = solar.best_speed(lap_length) + 24
                print(f"Travelling at driving speed of {velocity}")
        
            solar.update_capacity(velocity, length, angle)
            dist_left -= length
            lap_time = length / velocity
            curr_time += lap_time
            print(f"Current SOC: {(solar.current_capacity * 100) / solar.capacity}")
            print(f"Distance remaining: {dist_left}")
            print(f"Lap time: {lap_time}\n")
        
    print(f"\n\nEnd capacity: {solar.current_capacity}")
    print(f"Total time: {curr_time}")
    return curr_time
    # print(f"Fastest Speed:  {high_velocity} km/h, Laps: {laps}")
    # print(f"Coasting Speed: {coast_velocity} km/h")
    # print(f"Total Distance: {distance} km")
    # print(f"Recharge time: {solar.calc_recharge_time():0.3f} hours")


# best_time = 100
# best_speed = 0
# car = construct()
# for speed in range(1, 91):
#     time = run(car, speed)
#     if time < best_time:
#         best_time = time
#         best_speed = speed
#     car.current_capacity = (car.capacity * car.start_soc) / 100

# print(f"Best time was {best_time} with a top speed of {best_speed}")
car = construct()
run(car, 90)