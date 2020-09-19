from car import Car
import inputs
from pint import UnitRegistry

ureg = UnitRegistry()
        
user_inputs = inputs.get_inputs()
carlito = Car(user_inputs)
print(carlito.tire_contribution())
print(carlito.power_consumption(30))
# print(carlito.mass.magnitude * 2.20462)
# carlito.update_capacity(90,6,0)
# print(carlito.current_capacity)