def GetInputs():
    file  = open('input.txt', 'r')          #read from input.txt
    inputs = {}                            #dictionary to store inputs
    while True:
        line = file.readline()
        line = line.strip()
        if not line:
            break
        var = line.split(" ")
        in_name = var[0][:-1]
        inputs[in_name] = float(var[-1])
    file.close()
    return inputs
#print(GetInputs())


