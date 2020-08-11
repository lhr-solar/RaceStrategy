import os

def get_inputs():
    inputs = {} #dictionary to store inputs
    directory_path = os.path.dirname(os.path.abspath(__file__)) 
    new_path = os.path.join(directory_path, "input.txt")
    
    with open(new_path) as f: # read from input.txt
        lines = f.readlines()
        for line in lines:
            var = line.strip().split(":")
            in_name = var[0]
            inputs[in_name] = float(var[1])
    f.close()
    return inputs


