def get_inputs():
    inputs = {} #dictionary to store inputs
    with open('input.txt') as f: # read from input.txt
        lines = f.readlines()
        for line in lines:
            print(line)
            var = line.strip().split(":")
            in_name = var[0]
            inputs[in_name] = float(var[1])
    f.close()
    return inputs


