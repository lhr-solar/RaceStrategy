import math # sin
import numpy as np

import sympy as sy

gravity = 9.81 # m/s^2

class Car:
    """A class representing the solar car
    
    This class stores all characteristics of the car, such as the battery levels and dynamic
    coefficients. It has access to race strategy functions that can determine desired speeds
    based on certain conditions, as well as functions to update values of the car
    such as capacity or energy.

    Attributes:
        max_speed: an int representing the fastest speed the car can reach
        start_soc: a percentage representing the starting state of charge of the batteries
        end_soc: a percentage representing the desired end state of charge of the batteries
        capacity: an int of the total capacity of the batteries in KWh
        mass: an int of the mass of the car in kg 
        rolling_resistance: a float of the rolling resistance constant of the car
        drag_c: a float of the drag coefficient of the car
        cross_area: a float of the front cross sectional area of the car in m^2
        recharge_rate: a float representing how much power the solar cells generate in KWh
        current_capacity: a float that stores the current capacity of the batteries during the simulation in KWh
        end_capacity: a float that stores the desired end capacity of the batteries in KWh
    """
    def __init__(self, inputs, recharge_rate = 0.8):

        self.max_speed          = int(inputs["max_speed"])     # kph
        self.max_accel          = float(inputs["max_accel"])   # m/s^2
        self.start_soc          = inputs["start_soc"]          # %, soc = state of charge
        self.end_soc            = inputs["end_soc"]            # %, what we want the soc to be at the end
        self.capacity           = inputs["capacity"]           # KWh
        self.mass               = inputs["mass"]               # kg
        self.rolling_resistance = inputs["rolling_resistance"] # average for car tires on asphalt
        self.drag_c             = inputs["drag_coefficient"]   # from thiago
        self.cross_area         = inputs["cross_area"]         # m^2, from thiago
        self.recharge_rate      = recharge_rate                # kW           

        self.current_capacity   = (self.start_soc * self.capacity) / 100 # KWh
        self.start_capacity     = (self.start_soc * self.capacity) / 100 # KWh
        self.end_capacity       = (self.end_soc   * self.capacity) / 100 # KWh
    

    # gives the best speed we can run
    def best_speed(self, time, angle):
        """
        Takes a distance and calculates the best speed the car can currently drive at.
        
        Args:
            distance: A value indicating the distance to calculate the speed with.
            time: In hours
        
        Returns:
            A speed, in kph, that the car should travel at to achieve maximum efficiency.
        """
        for velocity in range(self.max_speed, 0, -1): # velocity in km/h
            delta_energy = time * (self.recharge_rate - self.motor_power(velocity, angle)) #kWh

            if (self.current_capacity + delta_energy) >= self.end_capacity:
                return velocity
    

    def coast_speed(self, angle):
        """
        Takes a distance and calculates the best coasting speed the car can currently drive at. 
        This speed will be something within the range of being able to power the car 
        on mainly solar power so the battery is able to recharge while driving.
        
        Args:
            distance: A value indicating the distance to calculate the speed with.
        
        Returns:
            A speed, in kph, that the car should travel at to recharge its batteries with.
        """
        
        if (abs(angle) > 0.5): # big road grade change
            return self.coast_speed(0)
            
        for velocity in range(int(self.max_speed), 0): # velocity in km/h
            net_power = self.recharge_rate - self.motor_power(velocity, angle) # kW

            if (net_power > 0): # find best coasting speed
                return velocity
        
        return 0


    # return time to recharge battery while coasting(default charges to 80%)
    def calc_recharge_time(self, upper_battery_capacity = 4):
        """
        Takes a total distance and calculates the time it would take for the car 
        to recharge its batteries to the given capacity. Assumes that 
        the car is travelling at the optimized coasting speed
        
        Args:
            upper_battery_capacity: The battery capacity the car should recharge to.
            lap_length: The distance of one lap, in km.
            distance: The total distance for the car to travel, in km.
        
        Returns:
            A time, in hours, that the car would take to recharge its batteries while driving.
        
        """
        # coasting_velocity = self.coast_speed(lap_length, angle) # KWh, point when to swap back to battery power
        time  = ((upper_battery_capacity - self.current_capacity) / 
                (self.recharge_rate))
        return time


    def update_capacity(self, curr_velocity, time, angle):
        """
        Takes the current velocity the car is travelling at and a distance that 
        the car travelled over to calculate how much power was used. This updates
        the current capacity of the car acccordingly.
        
        Args:
            curr_velocity: The current velocity that the car is driving at.
            distance: The distance that the car travelled within this section, in km.
        
        """
        gained_energy = self.recharge_rate * time # KWh 
        
        energy = self.motor_power(curr_velocity, angle) * time

        self.current_capacity += gained_energy - energy


    ### DYNAMICS EQUATIONS ###

    def motor_power(self, velocity, angle):
        """
        Uses a velocity, distance, and gradient angle of the road to determine
        how much power is needed to drive the motor.

        This calculates the power needed based on rolling resistance, hill climbing,
        and air drag for the vehicle.
        
        Args:
            velocity: The desired speed the car should travel at.
            distance: The distance to travel at the given speed.
            angle: The gradient angle of the road that the car travels over.
        
        """

        # TODO: calculate based on speed/acceleration
        efficiency = 0.95

        power = (self.power_consumption(velocity) + 
                 self.hill_climb(velocity, angle) + 
                 self.air_drag(velocity)) / (efficiency * 1000) # kW

        return power # kW


    # hill climb = Power due to climb = W*V*sin(inclination);
    def hill_climb(self, velocity, angle):
        """
        Calculates how much power is needed to climb up a slope depending on the 
        current velocity and the gradient angle of the road.

        power = mass * gravity * velocity * sin(angle)
        
        Args:
            velocity: The desired speed the car should travel at.
            angle: The gradient angle of the road that the car travels over.
        
        """

        velocity *= (5/18) # k/h to m/s
        power = self.mass * gravity * velocity * math.sin(angle * (math.pi)/180) # watts
        
        if power < 0:
            return 0

        return power # W
    

    # air drag = P = 0.5*rho*Cd*A*V^3
    def air_drag(self, velocity):
        """
        Calculates how much power is needed to overcome air drag based on the 
        current velocity of the car.

        power = 0.0386 * air density * drag coefficient * cross sectional area * velocity^3
        
        Args:
            velocity: The desired speed the car should travel at.
        
        """

        velocity *= (5/18) # k/h to m/s

        # This is for sea level at standard temperature/pressure
        # TODO: update for COTA
        # air_density = 1.225 # kg/m^3
        air_density = 1.1839
        # TODO: combine d and cross_area into cda
        power = 0.5 * air_density * self.drag_c * self.cross_area * velocity**3 # watts
        return power # W
        

    # p0 = pressure of the tire at which the rolling resistance experiment was conducted
    # p  = max safe pressure || whatever pressure we assign​
    # d0 = actual diameter of the wheel
    # dw = diameter of wheel w/o tire influence
    # weight of car is 600 pounds
    # 60% front || 40% back
    # Results of Rolling Resistance: Graph of Power Consumption at Different Velocities, Different Air Pressure
    # Constants && Assumptions used for the Following Calculations:
    # d0 = 21.67 in = 0.5504 meters (actual diameter)
    # dw = 16    in = 0.4064 meters (advertised nominal diameter)
    # Total Weight of car will be 600 lbs: 60% front || 40% back
    # p0 = 80 psi
    # p  = 75 psi
    # K  = 2.47 (derived from experimental data), pounds force / inch
    # V  = velocity of the vehicle
    # ALL values must be in SI units
    def tire_contribution(self, K = 2.47, d0 = 21.67, dw = 16, p = 75, p0 = 80):
        N = (self.mass * 2.20462)  # normal force, convert kg to lbs = mg
        h = (0.5 * (d0/dw) * math.pow((p/p0), 0.3072) * \
                (dw - math.pow(math.pow(dw, 2) - (4 * N/math.pi) * \
                ((2.456 + 0.251 * dw) / (19.58 + 0.5975 * p)), 0.5))) # should be a unit inches
        return (h * K * 4.44822) # rolling resistance force, converted lb-force to newtons

    # ​self, K,d0,dw,p,p0,N,V
    def power_consumption(self, V):
        V *= (5/18) # k/h to m/s
        return (self.tire_contribution() * V) # W

import inputs
user_inputs = inputs.get_inputs()

car = Car(user_inputs)
car.coast_speed(3)