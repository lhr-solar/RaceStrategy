"""
main.py
====================================
The core module of the Lap Simulator
"""

# main script for running race strat software

from solarpanel.main import main as solar_power
from battery.IO import *
inputs = GetInputs()

lap_length = inputs['lap_length'] # in kilometers
laps       = int(inputs['laps'])
distance   = lap_length * laps
gravity    = 9.81  #m/s^2


class Car:          #starts at 50% only uses 2%
    """A class representing the solar car"""
    def __init__(self, max_speed = 90, start_soc = 50, end_soc = 48, 
                 capacity = 5, mass = 227, rolling_resistance = 0.020, 
                 drag_coefficient = 0.256, cross_area = 1.2):

        self.max_speed          = int(inputs['max_speed'])    # kph
        self.start_soc          = inputs['start_soc']         # %, soc = state of charge
        self.end_soc            = inputs['end_soc']           # %, what we want the soc to be at the end
        self.capacity           = inputs['capacity']          # KWh
        self.mass               = inputs['mass']              # kg
        self.rolling_resistance = inputs['rolling_resistance']# average for car tires on asphalt
        self.drag_coefficient   = inputs['drag_coefficient']  # from thiago
        self.cross_area         = inputs['cross_area']        # m^2, from thiago
        self.recharge_rate      = solar_power()
        print(f"recharge rate = {self.recharge_rate}")

        self.current_capacity   = (start_soc * capacity) / 100 #KWh
        self.end_capacity       = (end_soc   * capacity) / 100 # KWh
    

    # gives the best speed we can run
    def best_speed(self, distance):
        """
        Return the best speed the car can currently drive at over the given distance.
        Parameters
        ----------
        distance
            A value indicating the distance to calculate the speed with.
        """
        acceleration   = 0
        gradient_angle = 0     #
        air_density    = 1.225 # kg/m^3

        for velocity in range(self.max_speed, 0, -1): # velocity in km/h
            time = distance / velocity
            gained_energy = self.recharge_rate * time # KWh 
            energy = (1/3600) * distance * ((self.mass * gravity * self.rolling_resistance) +
                    (0.0386 * air_density * self.drag_coefficient * self.cross_area * velocity ** 2) + # 0.0386 for km/h
                    (self.mass * acceleration))

            if (self.current_capacity - energy + gained_energy) >= self.end_capacity:
                return velocity
    

    def coast_speed(self, distance):
        acceleration   = 0
        gradient_angle = 0     #
        air_density    = 1.225 # kg/m^3

        for velocity in range(1, self.max_speed): # velocity in km/h
            time = distance / velocity
            gained_energy = self.recharge_rate * time # KWh 
            energy = (1/3600) * distance * ((self.mass * gravity * self.rolling_resistance) +
                    (0.0386 * air_density * self.drag_coefficient * self.cross_area * velocity ** 2) + # 0.0386 for km/h
                    (self.mass * acceleration))

            if (energy > gained_energy): # find best coasting speed
                return velocity - 5

    # return time to recharge battery while coasting(default charges to 80%)
    def calc_recharge_time(self, upper_battery_capacity = 4):
        acceleration = 0
        air_density  = 1.225 # kg/m^3

        coasting_velocity = self.coast_speed(lap_length) # KWh, point when to swap back to battery power
        time  = ((upper_battery_capacity - self.current_capacity) / 
                (self.recharge_rate - ((1/3600) * coasting_velocity * ((self.mass * gravity * self.rolling_resistance) +
                (0.0386 * air_density * self.drag_coefficient * self.cross_area * coasting_velocity ** 2) +
                (self.mass * acceleration)))))
        return time

    def update_capacity(self, curr_velocity, distance):
        air_density    = 1.225 # kg/m^3
        time = distance / curr_velocity
        acceleration   = 0


        gained_energy = self.recharge_rate * time # KWh 
        
        energy = (1/3600) * distance * ((self.mass * gravity * self.rolling_resistance) +
                    (0.0386 * air_density * self.drag_coefficient * self.cross_area * curr_velocity ** 2) + # 0.0386 for km/h
                    (self.mass * acceleration))
        self.current_capacity += gained_energy - energy
        


def main():
    # energy = 4.5 = 1/3600*[230*9.8*0.02 + 0.0386*1.225*0.25*2*v^2 ]*50

    solar = Car()
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