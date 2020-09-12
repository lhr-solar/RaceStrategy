from car import Car
import inputs

user_inputs = inputs.get_inputs()
carlito = Car(user_inputs)
print(carlito.current_capacity)
carlito.update_capacity(90,6,0)
print(carlito.current_capacity)