"""
main.py
====================================
The core module of the Lap Simulator
"""

import math
import sys
import csv
import inputs
import strats
import os

from shutil          import copyfile
from io              import StringIO
from solarpanel.main import main as solar_power
from car             import Car

# TODO: make this a configurable parameter
sim_step_time = 0.0025 # hr

user_inputs = inputs.get_inputs()
# lap_length = user_inputs["lap_length"] # km
lap_length    = 0
accl          = 300 #kph^2
laps          = int(user_inputs['laps'])
lap_print     = user_inputs['show_laps']
section_print = user_inputs['show_section']

solar_panel_power = []

solar_panel_power = solar_power(float(user_inputs['cloud_coverage']), str(user_inputs['starting_time']), 0, 12) # 0.xx for simulating data, 1 for weather scraping

track = []

with open("track.txt") as f:
    lines = f.readlines()
    for line in lines:
        var         = line.strip().split(",")
        length      = float(var[0])
        lap_length += length
        angle       = float(var[1])
        track.append([length, angle])
f.close()

distance = lap_length * laps

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
    return solar


def run(solar, max_speed, strat):
    race_time      = 0
    dist_left      = distance
    velocity_avg   = 0
    min_velocity   = 1000
    max_velocity   = -1  
    old_velocity   = 0
    with open('temp.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        column_names = [strat+'-Time', strat+'-Velocity', strat+'-SOC', 
                        strat+'=Air Drag', strat+'-Hill Climb', 
                        strat+'-Rolling Resistance', strat+'-Angle', 
                        strat+'-Distance Remaining', strat+'-Straight Number']

        writer.writerow(column_names)

        solar.recharge_rate = solar_panel_power[0]
        if solar.recharge_rate == 0:
            solar.recharge_rate = 0.1
        
        lap           = 0
        straight_num  = 0
        straight_dist = track[straight_num][0]
        angle         = track[straight_num][1]
        allow_accl    = accl * sim_step_time # The amount our velocity can differ each step
        while(dist_left > 0):
            if(straight_dist <= 0):
                straight_num  = (straight_num + 1) % len(track)
                if straight_num == 0:
                    lap += 1
                straight_dist = track[straight_num][0] + straight_dist
                angle         = track[straight_num][1]
            result = getattr(strats, strat)(solar, max_speed, angle, sim_step_time, dist_left, straight_num, old_velocity, allow_accl)
            
            velocity = result[1]
            old_velocity = result[2]

            velocity = min(velocity, old_velocity + allow_accl)
            velocity = max(velocity, old_velocity - allow_accl)
            old_velocity = velocity

            velocity_avg += velocity * sim_step_time
            min_velocity = min(min_velocity, velocity)
            max_velocity = max(max_velocity, velocity)

            dist_left -= velocity * sim_step_time
            straight_dist -= velocity * sim_step_time

            solar.recharge_rate = solar_panel_power[int(race_time) % 12]
            if solar.recharge_rate == 0:
                solar.recharge_rate = 0.1
            solar.update_capacity(velocity, sim_step_time, angle)

            current_soc        = (solar.current_capacity * 100) / solar.capacity
            air_drag           = sim_step_time * solar.air_drag(velocity)
            hill_climb         = sim_step_time * solar.hill_climb(velocity, angle)
            rolling_resistance = sim_step_time * solar.power_consumption(velocity)
            
            race_time += sim_step_time
            writer.writerow([race_time, velocity, current_soc, air_drag, hill_climb, rolling_resistance, angle, dist_left, straight_num])

    velocity_avg /= race_time

    print(f"\nEnd capacity: {round(solar.current_capacity,3)} kwh")
    print(f"Total time: {round(race_time, 3)} hrs\n")
    print(f"Peak    Velocity: {round(max_velocity, 3)} km/h")
    print(f"Min     Velocity: {round(min_velocity, 3)} km/h")
    print(f"Average velocity: {round(velocity_avg, 3)} km/h\n")
    print(f"Recharge rate:    {solar.recharge_rate} kW/h")

    return race_time


strat_list = user_inputs['strategy'].split(",") # account for commas
if ("all" in strat_list[0].lower()):
    directory_path = os.path.dirname(os.path.abspath(__file__)) 
    new_path = os.path.join(directory_path, "stratlist.txt")
    
    strat_list.clear()
    with open(new_path) as f: # read from input.txt
        lines = f.readlines()
        for line in lines:
            strat_list.append(line.strip())
    f.close()
    
for strat in strat_list:
    best_time   = 10000000
    best_speed  = 0
    best_buffer = 0

    car = construct()
    test = ""
    old_stdout = sys.stdout # saves terminal stdout
    top_speed  = 60 if laps >= 20 else 91 #TODO: add config for this in input.txt

    print(f"\nTESTING STRAT: {strat}")
    for speed in range(35, top_speed):
        new_stdout = StringIO() # create new buffer to catch print outs
        sys.stdout = new_stdout # set system stdout to this buffer
        # try:
        time = run(car, speed, strat)
        # except:
        #     print(f"{new_stdout.getvalue()}")
        if time < best_time:
            best_time   = time
            best_speed  = speed
            best_buffer = new_stdout # save buffer if it was the best time
            copyfile('temp.csv', strat + '.csv')
        car.current_capacity = (car.capacity * car.start_soc) / 100

    sys.stdout = old_stdout # reset stdout to terminal to print final output
    print(f"{best_buffer.getvalue()}")
    print(f"Best time was {best_time} with a top speed of {best_speed}")
    best_buffer.close()
