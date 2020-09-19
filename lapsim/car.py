import math # sin
import numpy as np

from pint   import UnitRegistry
from config import ureg

gravity = 9.81 * ureg.meter / (ureg.second ** 2) # m/s^2

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

        self.max_speed          = int(inputs["max_speed"]) * ureg.kilometer / ureg.hours   # kph
        self.start_soc          = inputs["start_soc"]                                      # %, soc = state of charge
        self.end_soc            = inputs["end_soc"]                                        # %, what we want the soc to be at the end
        self.capacity           = inputs["capacity"]       * ureg.kilowatt_hour            # KWh
        self.mass               = inputs["mass"]           * ureg.kilogram                 # kg
        self.rolling_resistance = inputs["rolling_resistance"]                             # average for car tires on asphalt
        self.drag_c             = inputs["drag_coefficient"]                               # from thiago
        self.cross_area         = inputs["cross_area"]     * (ureg.meter ** 2)             # m^2, from thiago
        self.recharge_rate      = recharge_rate            * ureg.kilowatt                 # kW           

        self.current_capacity   = (self.start_soc * self.capacity) / 100 * ureg.kilowatt_hour # KWh
        self.end_capacity       = (self.end_soc   * self.capacity) / 100 * ureg.kilowatt_hour # KWh
    

    # gives the best speed we can run
    def best_speed(self, distance, angle):
        """
        Takes a distance and calculates the best speed the car can currently drive at.
        
        Args:
            distance: A value indicating the distance to calculate the speed with.
        
        Returns:
            A speed, in kph, that the car should travel at to achieve maximum efficiency.
        """
        # acceleration   = 0
        # air_density    = 1.225 # kg/m^3

        for velocity in range(self.max_speed, 0, -1): # velocity in km/h
            time = distance / velocity
            gained_energy = self.recharge_rate * time # KWh 
            energy = self.motor_energy(velocity, distance, angle)
            # energy = (1/3600) * distance * ((self.mass * gravity * self.rolling_resistance) +
            #         (0.0386 * air_density * self.drag_c * self.cross_area * velocity ** 2) + # 0.0386 for km/h
            #         (self.mass * acceleration))

            if (self.current_capacity - energy + gained_energy) >= self.end_capacity:
                return velocity
    

    def coast_speed(self, distance, angle):
        """
        Takes a distance and calculates the best coasting speed the car can currently drive at. 
        This speed will be something within the range of being able to power the car 
        on mainly solar power so the battery is able to recharge while driving.
        
        Args:
            distance: A value indicating the distance to calculate the speed with.
        
        Returns:
            A speed, in kph, that the car should travel at to recharge its batteries with.
        """
        # acceleration   = 0
        # air_density    = 1.225 # kg/m^3
        
        if (abs(angle) > 0.5): # big road grade change
            return self.coast_speed(distance, 0)
            # flat_energy = self.motor_energy(flat_v, distance, 0)
            # # test_energy = (1/3600) * distance * ((self.mass * gravity * self.rolling_resistance) +\
            # #         (self.mass * gravity * -20.365 * math.sin(angle))/1000 + \
            # #         (0.0386 * air_density * self.drag_c * self.cross_area * -20.365**3)/1000)
            # coeffs = [(0.0386 * air_density * self.drag_c * self.cross_area)/1000, 0, (self.mass * gravity * math.sin(angle*(math.pi)/180))/1000, \
            #         (self.mass * gravity * self.rolling_resistance - (flat_energy*3600)/distance)]
            # sol = np.roots(coeffs)
            # print(sol)
            # for item in sol:
            #     if item.imag == 0:
            #         item = item.real
            #     if type(item) == "complex" or item < 0:
            #         continue
            #     else:
            #         print(item)
            #         return item
        
            
        for velocity in range(1, self.max_speed): # velocity in km/h
            time = distance / (velocity*ureg.kilometer/ureg.hours)
            gained_energy = self.recharge_rate * time # KWh 
            energy = self.motor_energy(velocity, distance, angle)
            # energy = (1/3600) * distance * ((self.mass * gravity * self.rolling_resistance) +
            #         (0.0386 * air_density * self.drag_c * self.cross_area * velocity ** 2) + # 0.0386 for km/h
            #         (self.mass * acceleration))

            if (energy >= gained_energy): # find best coasting speed
                # print("found velocity")
                return velocity - 5
        # print("returning max speed")
        return self.max_speed


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


    def update_capacity(self, curr_velocity, distance, angle):
        """
        Takes the current velocity the car is travelling at and a distance that 
        the car travelled over to calculate how much power was used. This updates
        the current capacity of the car acccordingly.
        
        Args:
            curr_velocity: The current velocity that the car is driving at.
            distance: The distance that the car travelled within this section, in km.
        
        """
        time = distance / curr_velocity

        gained_energy = self.recharge_rate * time # KWh 
        
        energy = self.motor_energy(curr_velocity, distance, angle)
        #self.current_capacity += gained_energy - energy
        self.current_capacity -= energy


    ### DYNAMICS EQUATIONS ###

    def motor_energy(self, velocity, distance, angle):
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
        # energy = (1/3600) * distance * ((self.mass * gravity * self.rolling_resistance) +
        #                 (0.0386 * air_density * self.drag_coefficient * self.cross_area * velocity ** 2) + # 0.0386 for km/h
        #                 (self.mass * acceleration))
        time = distance / velocity # hours

        energy = time * (self.power_consumption(velocity) + 
                         self.hill_climb(velocity, angle) + 
                         self.air_drag(velocity))

        return energy # kWh

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
        # using m/s for velocity
        power = self.mass * gravity * (velocity*(5/18)) * math.sin(angle * (math.pi)/180) # watts
        
        if power < 0:
            return 0

        return power / 1000 # kW
    
    # air drag = P = 0.5*rho*Cd*A*V^3
    def air_drag(self, velocity):
        """
        Calculates how much power is needed to overcome air drag based on the 
        current velocity of the car.

        power = 0.0386 * air density * drag coefficient * cross sectional area * velocity^3
        
        Args:
            velocity: The desired speed the car should travel at.
        
        """
        #using m/s for velocity
        air_density = 1.225 * ureg.kilogram / (ureg.meters ** 3)# kg/m^3
        power = 0.5 * air_density * self.drag_c * self.cross_area * (velocity*(5/18))**3 # watts
        return power / 1000 # kW

        

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
        N = (self.mass.magnitude * 2.20462)  # normal force, convert kg to lbs = mg
        h = (0.5 * (d0/dw) * math.pow((p/p0), 0.3072) * \
                (dw - math.pow(math.pow(dw, 2) - (4 * N/math.pi) * \
                ((2.456 + 0.251 * dw) / (19.58 + 0.5975 * p)), 0.5))) # should be a unit inches
        return (h * K * 4.44822) * ureg.newtons# rolling resistance force, converted lb-force to newtons

    # ​self, K,d0,dw,p,p0,N,V
    def power_consumption(self, V):
        return (self.tire_contribution() * V * 5/18) # kW
        