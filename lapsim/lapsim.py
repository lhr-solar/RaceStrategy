"""
main.py
====================================
The core module of the Lap Simulator
"""

import math
import sys
import csv
from shutil import copyfile
from io import StringIO

from solarpanel.main import main as solar_power
from car import Car
import inputs
import strats

user_inputs = inputs.get_inputs()
# lap_length = user_inputs["lap_length"] # km
lap_length    = 0
laps          = int(user_inputs['laps'])
lap_print     = user_inputs['show_laps']
section_print = user_inputs['show_section']

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
    #solar.recharge_rate = solar_power(float(user_inputs['cloud_coverage'])) # 0.xx for simulating data, 1 for weather scraping
    solar.recharge_rate = 0.8
    return solar

def run(solar, max_speed):
    race_time = 0
    dist_left = distance
    velocity_sum = 0
    velocity_count = 0
    min_velocity = 1000
    max_velocity = -1
    with open('temp.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Time', 'Velocity', 'SOC', 'Air Drag', 'Hill Climb', 'Rolling Resistance', 'Angle'])
        for lap in range(laps):
            lap_buffer = StringIO()
            # lap_buffer.write(f"--- LAP {lap} ---\n")
            count = 0
            lap_time = 0
            lap_start_soc = solar.current_capacity
            starting_soc = 0
            
            for straight in track:
                section_buffer = StringIO()
                length = straight[0]
                angle  = straight[1]
                section_buffer.write("\n")
                section_buffer.write(f"Lap {lap} - Section {count} - Angle {angle}\n")
                
                result = strats.carl(solar, max_speed, angle, length, count)
                
                # update velocity
                section_buffer.write(result[0]) # writing out buffer string
                velocity = result[1]            # getting new velocity
                velocity_sum += velocity
                velocity_count += 1
                
                # update times
                section_time  = length / velocity
                section_time += result[2] # updating section time (if pitted)
                lap_time     += section_time
                race_time    += section_time
                
                # update capacity and distance left
                solar.update_capacity(velocity, length, angle)
                dist_left -= length
                
                min_velocity = velocity if min_velocity > velocity else min_velocity
                max_velocity = velocity if max_velocity < velocity else max_velocity

                current_soc        = (solar.current_capacity * 100) / solar.capacity
                air_drag           = (1/3600) * distance * solar.air_drag(velocity)
                hill_climb         = (1/3600) * distance * solar.hill_climb(velocity, angle)
                rolling_resistance = (1/3600) * distance * solar.power_consumption(velocity)

                writer.writerow([race_time, velocity, current_soc, air_drag, hill_climb, rolling_resistance, angle])

                section_buffer.write(f"Current SOC:        {round(current_soc, 3)} %\n")
                section_buffer.write(f"Distance remaining: {round(dist_left, 3)} km\n")
                section_buffer.write(f"Section time:       {round(section_time * 60 * 60, 3)} sec\n")
                section_buffer.write(f"Section length:     {round(length, 3)} km\n")
                
                section_buffer.write(f"--- Power Consumptions ---\n")
                section_buffer.write(f"Air Drag:           {round(air_drag, 3)} kWh\n")
                section_buffer.write(f"Hill Climb:         {round(hill_climb, 3)} kWh\n")
                section_buffer.write(f"Rolling Resistance: {round(rolling_resistance, 3)} kWh\n")
                if(section_print):
                    print(section_buffer.getvalue())
                section_buffer.close()

                if count == 0:
                    starting_soc = current_soc

                count += 1
            
            lap_end_soc = solar.current_capacity
            lap_recharge = solar.recharge_rate * lap_time
            lap_loss = lap_start_soc + lap_recharge - lap_end_soc
            delta_soc = starting_soc - ((solar.current_capacity) * 100 / solar.capacity)

            lap_buffer.write(f"\n--- Lap {lap} Results ---\n")
            lap_buffer.write(f"Lap Time:      {round((lap_time * 60), 3)} min\n")
            lap_buffer.write(f"Power Gains:   {round(lap_recharge, 3)} kWh\n")
            lap_buffer.write(f"Power Losses:  {round(lap_loss, 3)} kWh\n")
            lap_buffer.write(f"End SOC:       {round((solar.current_capacity * 100) / solar.capacity, 3)} %\n")
            lap_buffer.write(f"Change in SOC: {round(delta_soc, 3)} %\n")
            lap_buffer.write("\n")
            # race_time += lap_time

            if (lap_print):
                print(lap_buffer.getvalue())  
            lap_buffer.close()

    print(f"\nEnd capacity: {round(solar.current_capacity,3)} kwh")
    print(f"Total time: {round(race_time, 3)} hrs\n")
    print(f"Peak    Velocity: {round(max_velocity, 3)} km/h")
    print(f"Min     Velocity: {round(min_velocity, 3)} km/h")
    print(f"Average velocity: {round((velocity_sum / velocity_count), 3)} km/h\n")
    print(f"Recharge rate:    {solar.recharge_rate} kW/h")
    return race_time
    # print(f"Fastest Speed:  {high_velocity} km/h, Laps: {laps}")
    # print(f"Coasting Speed: {coast_velocity} km/h")
    # print(f"Total Distance: {distance} km")
    # print(f"Recharge time: {solar.calc_recharge_time():0.3f} hours")


best_time = 10000000
best_speed = 0
best_buffer = 0

car = construct()
test = ""
old_stdout = sys.stdout # saves terminal stdout

for speed in range(20, 91):
    new_stdout = StringIO() # create new buffer to catch print outs
    sys.stdout = new_stdout # set system stdout to this buffer
    time = run(car, speed)
    if time < best_time:
        best_time = time
        best_speed = speed
        best_buffer = new_stdout # save buffer if it was the best time
        copyfile('temp.csv', 'sim.csv')
    car.current_capacity = (car.capacity * car.start_soc) / 100

sys.stdout = old_stdout # reset stdout to terminal to print final output
print(f"{best_buffer.getvalue()}")
# print(f"Best time was {best_time} with a top speed of {best_speed}")
best_buffer.close()
# car = construct()
# run(car, 90)
