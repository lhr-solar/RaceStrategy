import math

gravity = 9.81 # m/s^2

class Car:          #starts at 50% only uses 2%
    """A class representing the solar car"""
    def __init__(self, inputs, recharge_rate = 0.8):

        self.max_speed          = int(inputs["max_speed"]) # kph
        self.start_soc          = inputs["start_soc"] # %, soc = state of charge
        self.end_soc            = inputs["end_soc"] # %, what we want the soc to be at the end
        self.capacity           = inputs["capacity"] # KWh
        self.mass               = inputs["mass"] # kg
        self.rolling_resistance = inputs["rolling_resistance"] # average for car tires on asphalt
        self.drag_c             = inputs["drag_coefficient"] # from thiago
        self.cross_area         = inputs["cross_area"] # m^2, from thiago
        self.recharge_rate      = recharge_rate

        self.current_capacity   = (self.start_soc * self.capacity) / 100 # KWh
        self.end_capacity       = (self.end_soc   * self.capacity) / 100 # KWh
    

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
                    (0.0386 * air_density * self.drag_c * self.cross_area * velocity ** 2) + # 0.0386 for km/h
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
                    (0.0386 * air_density * self.drag_c * self.cross_area * velocity ** 2) + # 0.0386 for km/h
                    (self.mass * acceleration))

            if (energy > gained_energy): # find best coasting speed
                return velocity - 5

    # return time to recharge battery while coasting(default charges to 80%)
    def calc_recharge_time(self, upper_battery_capacity = 4, lap_length = 5, distance = 5):
        acceleration = 0
        air_density  = 1.225 # kg/m^3

        coasting_velocity = self.coast_speed(lap_length) # KWh, point when to swap back to battery power
        time  = ((upper_battery_capacity - self.current_capacity) / 
                (self.recharge_rate - self.motor_energy(coasting_velocity, distance, 0)))
        return time

    def update_capacity(self, curr_velocity, distance):
        air_density    = 1.225 # kg/m^3
        time = distance / curr_velocity
        acceleration   = 0


        gained_energy = self.recharge_rate * time # KWh 
        
        energy = self.motor_energy(curr_velocity, distance, 0)
        self.current_capacity += gained_energy - energy

    ### DYNAMICS EQUATIONS ###

    def motor_energy(self, velocity, distance, angle):
        # energy = (1/3600) * distance * ((self.mass * gravity * self.rolling_resistance) +
        #                 (0.0386 * air_density * self.drag_coefficient * self.cross_area * velocity ** 2) + # 0.0386 for km/h
        #                 (self.mass * acceleration))
        energy = (1/3600) * distance * (self.rolling_resist() + 
                                        self.hill_climb(velocity, angle) + 
                                        self.air_drag(velocity))
        return energy

    # rolling resistance
    def rolling_resist(self):
        power = self.mass * gravity * self.rolling_resistance
        return power

    # hill climb = Power due to climb = W*V*sin(inclination);
    def hill_climb(self, velocity, angle):
        power = self.mass * gravity * velocity * math.sin(angle) # watts
        return power / 1000 # kW
    
    # air drag = P = 0.5*rho*Cd*A*V^3
    def air_drag(self, velocity):
        air_density = 1.225 # kg/m^3
        power = 0.0386 * air_density * self.drag_c * self.cross_area * velocity**2 # watts
        return power / 1000 # kW