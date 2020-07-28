# main script for running race strat software
lap_length = 5.513 # in kilometers
laps       = 1
distance   = lap_length * laps
gravity    = 9.81  #m/s^2

class Car:          #starts at 50% only uses 2%
    def __init__(self, max_speed = 90, start_soc = 50, end_soc = 48, 
                 capacity = 5, mass = 227, rolling_resistance = 0.020, 
                 drag_coefficient = 0.256, cross_area = 1.2, recharge_rate = 0.8):

        self.max_speed          = max_speed          # kph
        self.start_soc          = start_soc          # %, soc = state of charge
        self.end_soc            = end_soc            # %, what we want the soc to be at the end
        self.capacity           = capacity           # KWh
        self.mass               = mass               # kg
        self.rolling_resistance = rolling_resistance # average for car tires on asphalt
        self.drag_coefficient   = drag_coefficient   # from thiago
        self.cross_area         = cross_area         # m^2, from thiago
        self.recharge_rate      = recharge_rate

        self.current_capacity   = (start_soc * capacity) / 100
        self.end_capacity       = (end_soc   * capacity) / 100 # KWh
    

    # gives the best speed we can run
    def best_speed(self):
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
    

    def coast_speed(self):
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
                return velocity - 1

    # return time to recharge battery while coasting(default charges to 80%)
    def calc_recharge_time(self, upper_battery_capacity = 4):
        acceleration = 0
        air_density  = 1.225 # kg/m^3

        coasting_velocity = self.coast_speed() # KWh, point when to swap back to battery power
        time  = ((upper_battery_capacity - self.current_capacity) / 
                (self.recharge_rate - ((1/3600) * coasting_velocity * ((self.mass * gravity * self.rolling_resistance) +
                (0.0386 * air_density * self.drag_coefficient * self.cross_area * coasting_velocity ** 2) +
                (self.mass * acceleration)))))
        return time



def main():
    # energy = 4.5 = 1/3600*[230*9.8*0.02 + 0.0386*1.225*0.25*2*v^2 ]*50
    
    solar = Car()
    high_velocity = solar.best_speed()
    coast_velocity = solar.coast_speed()
    print(f"Fastest Speed:  {high_velocity} km/h, Laps: {laps}")
    print(f"Coasting Speed: {coast_velocity} km/h")
    print(f"Total Distance: {distance} km")
    print(f"Recharge time: {solar.calc_recharge_time():0.3f} hours")

main()
