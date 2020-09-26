import inputs
import strats
from car    import Car
from pint   import UnitRegistry
from config import ureg

        
user_inputs = inputs.get_inputs()
carlito = Car(user_inputs)
# print(carlito.current_capacity)
# print(carlito.update_capacity(20, 5, 0))
v = 30 * ureg.kilometers / ureg.hours
length = 5 * ureg.kilometers
angle = 5 * ureg.degrees
result = strats.carl(carlito, v, 0, length, angle)
velocity = result[1] 
# print(velocity)
print(f"Motor energy: {carlito.motor_energy(v, length, angle)}\n")
print(f"Power consumption: {carlito.power_consumption(v)}\n")
print(f"Hill climb:        {carlito.hill_climb(v, angle)}\n")
print(f"Air drag:          {carlito.air_drag(v)}\n")
# print(carlito.mass.magnitude * 2.20462)
carlito.update_capacity(v,length,angle)
# print(carlito.current_capacity)